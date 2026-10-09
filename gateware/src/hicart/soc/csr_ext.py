from collections import defaultdict
from amaranth import *
from amaranth import Module
from amaranth.lib import enum, wiring
from amaranth.lib.wiring import In, Out, flipped
from amaranth.utils import ceil_log2, exact_log2

from amaranth_soc import csr, wishbone
from amaranth_soc.csr.bus import Signature, Interface, Element
from amaranth_soc.csr.reg import Register
from amaranth_soc.memory import MemoryMap


class Multiplexer(wiring.Component):
    class _Shadow:
        class Chunk:
            """The interface between a CSR multiplexer and a shadow register chunk."""
            def __init__(self, shadow, offset, registers):
                self.name = f"{shadow.name}__{offset}"
                self.data = Signal(shadow.granularity, name=f"{self.name}__data")
                self.r_en = Signal(name=f"{self.name}__r_en")
                self.w_en = Signal(name=f"{self.name}__w_en")
                self._registers = tuple(registers)

            def registers(self):
                """Iterate the address ranges of CSR registers using this chunk."""
                yield from self._registers

        """CSR multiplexer shadow register.

        Attributes
        ----------
        name : :class:`str`
            Name of the shadow register.
        granularity : :class:`int`
            Amount of bits stored in a chunk of the shadow register.
        overlaps : :class:`int`
            Maximum number of CSR registers that can share a shadow register chunk. Optional.
            If ``None``, it is implicitly set by :meth:`Multiplexer._Shadow.prepare`.
        """
        def __init__(self, granularity, overlaps, *, name):
            assert isinstance(name, str)
            assert isinstance(granularity, int) and granularity >= 0
            assert overlaps is None or isinstance(overlaps, int) and overlaps >= 0
            self.name        = name
            self.granularity = granularity
            self.overlaps    = overlaps
            self._ranges     = set()
            self._size       = 1
            self._chunks     = None

        @property
        def size(self):
            """Size of the shadow register.

            Returns
            -------
            :class:`int`
                The amount of :class:`Multiplexer._Shadow.Chunk`s of the shadow. It can increase
                by calling :meth:`Multiplexer._Shadow.add` or :meth:`Multiplexer._Shadow.prepare`.
            """
            return self._size

        def add(self, reg_range):
            """Add a CSR register to the shadow.

            Arguments
            ---------
            reg_range : :class:`range`
                Address range of a CSR register. It uses ``2 ** ceil_log2(reg_range.stop -
                reg_range.start)`` chunks of the shadow register. If this amount is greater than
                :attr:`~Multiplexer._Shadow.size`, it replaces the latter.
            """
            assert isinstance(reg_range, range)
            self._ranges.add(reg_range)
            reg_size   = 2 ** ceil_log2(reg_range.stop - reg_range.start)
            self._size = max(self._size, reg_size)

        def decode_address(self, addr, reg_range):
            """Decode a CSR bus address into a shadow register offset.

            Returns
            -------
            :class:`int`
                The shadow register offset corresponding to the :class:`Multiplexer._Shadow.Chunk`
                used by ``addr``.

                The address decoding scheme is illustrated by the following example:
                    * ``addr`` is ``0x1c``;
                    * ``reg_range`` is ``range(0x1b, 0x1f)``;
                    * the :attr:`~Multiplexer._Shadow.size` of the shadow is ``16``.

                The lower bits of the offset would be ``0b00``, extracted from ``addr``:

                .. code-block::

                    +----+--+--+
                    |0001|11|00|
                    +----+--+--+
                            │  └─ 0
                            └──── ceil_log2(reg_range.stop - reg_range.start)

                The upper bits of the offset would be ``0b10``, extracted from ``reg_range.start``:

                .. code-block::

                    +----+--+--+
                    |0001|10|11|
                    +----+--+--+
                         │  │
                         │  └──── ceil_log2(reg_range.stop - reg_range.start)
                         └─────── log2(self.size)

                The decoded offset would therefore be ``8`` (i.e. ``0b1000``).
            """
            assert reg_range in self._ranges and addr in reg_range
            reg_size  = 2 ** ceil_log2(reg_range.stop - reg_range.start)
            self_mask = self.size - 1
            reg_mask  = reg_size - 1
            return reg_range.start & self_mask & ~reg_mask | addr & reg_mask

        def encode_offset(self, offset, reg_range):
            """Encode a shadow register offset into a CSR bus address.

            Returns
            -------
            :class:`int`
                The bus address in ``reg_range`` using the :class:`Multiplexer._Shadow.Chunk`
                located at ``offset``. See :meth:`~Multiplexer._Shadow.decode_address` for details.
            """
            assert reg_range in self._ranges and isinstance(offset, int)
            reg_size = 2 ** ceil_log2(reg_range.stop - reg_range.start)
            return reg_range.start + ((offset - reg_range.start) % reg_size)

        def prepare(self):
            """Balance out and instantiate the shadow register chunks.

            The scheme used by :meth:`~Multiplexer._Shadow.decode_address` allows multiple bus
            addresses to be decoded to the same shadow register offset. Depending on the platform
            and its toolchain, this may create nets with high fan-in (if the chunk is read from
            the bus) or fan-out (if written), which may impact timing closure or resource usage.

            If any shadow register offset is aliased to more bus addresses than permitted by the
            :attr:`~Multiplexer._Shadow.overlaps` constraint, the :attr:`~Multiplexer._Shadow.size`
            of the shadow is doubled. This increases the number of address bits used for decoding,
            which effectively balances chunk usage across the shadow register.

            This method is recursive until the overlap constraint is satisfied.
            """
            if isinstance(self._ranges, frozenset):
                return
            if self.overlaps is None:
                self.overlaps = len(self._ranges)

            registers = defaultdict(list)
            balanced  = True

            # sort ranges in an arbitrary but nice fashion so that we build registers and so create
            # chunks and elaborate their connections deterministically
            ranges = sorted(self._ranges, key=lambda r: (r.start, r.stop, r.step))
            for reg_range in ranges:
                for chunk_addr in reg_range:
                    chunk_offset = self.decode_address(chunk_addr, reg_range)
                    if len(registers[chunk_offset]) > self.overlaps:
                        balanced = False
                        break
                    registers[chunk_offset].append(reg_range)

            if balanced:
                self._ranges = frozenset(self._ranges)
                self._chunks = dict()
                for chunk_offset, chunk_registers in registers.items():
                    chunk = Multiplexer._Shadow.Chunk(self, chunk_offset, chunk_registers)
                    self._chunks[chunk_offset] = chunk
            else:
                self._size *= 2
                self.prepare()

        def chunks(self):
            """Iterate shadow register chunks used by at least one CSR register."""
            for chunk_offset, chunk in self._chunks.items():
                yield chunk_offset, chunk

    """CSR register multiplexer.

    An address-based multiplexer for CSR registers implementing atomic updates.

    This implementation assumes the following from the CSR bus:
        * an initiator must have exclusive ownership over the multiplexer for the full duration of
          a register transaction;
        * an initiator must access a register in ascending order of addresses, but it may abort a
          transaction after any bus cycle.

    Latency
    -------

    Writes are registered, and are performed 1 cycle after ``w_stb`` is asserted.

    Alignment
    ---------

    Because the CSR bus conserves logic and routing resources, it is common to e.g. access
    a CSR bus with an *n*-bit data path from a CPU with a *k*-bit datapath (*k>n*) in cases
    where CSR access latency is less important than resource usage. In this case, two strategies
    are possible for connecting the CSR bus to the CPU:
        * The CPU could access the CSR bus directly (with no intervening logic other than simple
          translation of control signals). In this case, the register alignment should be set
          to 1 (i.e. `memory_map.alignment` should be set to 0), and each *w*-bit register would
          occupy *ceil(w/n)* addresses from the CPU perspective, requiring the same amount of
          memory instructions to access.
        * The CPU could also access the CSR bus through a width down-converter, which would issue
          *k/n* CSR accesses for each CPU access. In this case, the register alignment should be
          set to *k/n*, and each *w*-bit register would occupy *ceil(w/k)* addresses from the CPU
          perspective, requiring the same amount of memory instructions to access.

    If the register alignment (i.e. `2 ** memory_map.alignment`) is greater than 1, it affects
    which CSR bus write is considered a write to the last register chunk. For example, if a 24-bit
    register is used with a 8-bit CSR bus and a CPU with a 32-bit datapath, a write to this
    register requires 4 CSR bus writes to complete and the 4th write is the one that actually
    writes the value to the register. This allows determining write latency solely from the amount
    of addresses the register occupies in the CPU address space, and the width of the CSR bus.

    Parameters
    ----------
    memory_map : :class:`..memory.MemoryMap`
        Memory map of CSR registers.
    shadow_overlaps : int
        Maximum number of CSR registers that can share a chunk of a shadow register.
        Optional. If ``None``, any number of CSR registers can share a shadow chunk.
        See :class:`Multiplexer._Shadow` for details.

    Attributes
    ----------
    bus : :class:`Interface`
        CSR bus providing access to registers.
    """
    def __init__(self, memory_map, *, shadow_overlaps=None, byteorder="little"):
        if byteorder not in ("little", "big"):
            raise ValueError("Byte order must be either little or big")
        self._check_memory_map(memory_map)
        self._r_shadow = self._Shadow(memory_map.data_width, shadow_overlaps, name="r_shadow")
        self._w_shadow = self._Shadow(memory_map.data_width, shadow_overlaps, name="w_shadow")
        super().__init__({
            "bus": In(Signature(addr_width=memory_map.addr_width,
                                data_width=memory_map.data_width))
        })
        self.bus.memory_map = memory_map
        self._byteorder = byteorder

    def _check_memory_map(self, memory_map):
        if not isinstance(memory_map, MemoryMap):
            raise TypeError(f"CSR multiplexer memory map must be an instance of MemoryMap, not "
                            f"{memory_map!r}")
        if list(memory_map.windows()):
            raise ValueError("CSR multiplexer memory map cannot have windows")
        for reg, reg_name, (reg_start, reg_end) in memory_map.resources():
            if not ("element" in reg.signature.members and
                    reg.signature.members["element"].flow == In and
                    reg.signature.members["element"].is_signature and
                    isinstance(reg.signature.members["element"].signature, Element.Signature)):
                raise AttributeError(f"Signature of CSR register {reg_name} must have a "
                                     f"csr.Element.Signature member named 'element' and oriented "
                                     f"as wiring.In")

    def elaborate(self, platform):
        m = Module()

        for reg, _, (reg_start, reg_end) in self.bus.memory_map.resources():
            reg_range = range(reg_start, reg_end)
            if reg.element.access.readable():
                self._r_shadow.add(reg_range)
            if reg.element.access.writable():
                self._w_shadow.add(reg_range)

        self._r_shadow.prepare()
        self._w_shadow.prepare()

        def calc_offset(reg_range, chunk_addr):
            if self._byteorder == "big":
                return reg_range.stop - chunk_addr - 1
            else:
                return chunk_addr - reg_range.start

        # Instead of a straightforward multiplexer for reads, use an address comparator for each
        # shadow register chunk, AND the comparator output with the chunk contents, and OR all of
        # those together. If the toolchain doesn't already synthesize multiplexer trees this way,
        # this trick can save a significant amount of logic, since e.g. one 4-LUT can pack one
        # 2-MUX, but two 2-AND or 2-OR gates.
        r_data_fanin = 0

        for chunk_offset, r_chunk in self._r_shadow.chunks():
            # Use the same trick to select which CSR register is read into a shadow register chunk.
            r_chunk_w_en_fanin = 0
            r_chunk_data_fanin = 0

            m.d.sync += r_chunk.r_en.eq(0)

            with m.Switch(self.bus.addr):
                for reg_range in r_chunk.registers():
                    chunk_addr = self._r_shadow.encode_offset(chunk_offset, reg_range)
                    reg        = self.bus.memory_map.decode_address(reg_range.start)
                    reg_offset = calc_offset(reg_range, chunk_addr)
                    reg_r_data = reg.element.r_data.word_select(reg_offset, self.bus.data_width)

                    with m.Case(chunk_addr):
                        if chunk_addr == reg_range.start:
                            m.d.comb += reg.element.r_stb.eq(self.bus.r_stb)
                        # Delay by 1 cycle, allowing reads to be pipelined.
                        m.d.sync += r_chunk.r_en.eq(self.bus.r_stb)

                    r_chunk_w_en_fanin |= reg.element.r_stb
                    r_chunk_data_fanin |= Mux(reg.element.r_stb, reg_r_data, 0)

            m.d.comb += r_chunk.w_en.eq(r_chunk_w_en_fanin)
            with m.If(r_chunk.w_en):
                m.d.sync += r_chunk.data.eq(r_chunk_data_fanin)

            r_data_fanin |= Mux(r_chunk.r_en, r_chunk.data, 0)

        m.d.comb += self.bus.r_data.eq(r_data_fanin)

        for chunk_offset, w_chunk in self._w_shadow.chunks():
            with m.Switch(self.bus.addr):
                for reg_range in w_chunk.registers():
                    chunk_addr = self._w_shadow.encode_offset(chunk_offset, reg_range)
                    reg        = self.bus.memory_map.decode_address(reg_range.start)
                    reg_offset = calc_offset(reg_range, chunk_addr)
                    reg_w_data = reg.element.w_data.word_select(reg_offset, self.bus.data_width)

                    if chunk_addr == reg_range.stop - 1:
                        m.d.sync += reg.element.w_stb.eq(0)

                    with m.Case(chunk_addr):
                        if chunk_addr == reg_range.stop - 1:
                            # Delay by 1 cycle, avoiding combinatorial paths through
                            # the CSR bus and into CSR registers.
                            m.d.sync += reg.element.w_stb.eq(self.bus.w_stb)
                        m.d.comb += w_chunk.w_en.eq(self.bus.w_stb)

                    m.d.comb += reg_w_data.eq(w_chunk.data)

            with m.If(w_chunk.w_en):
                m.d.sync += w_chunk.data.eq(self.bus.w_data)

        return m


class Bridge(wiring.Component):
    """CSR bridge.

    Parameters
    ----------
    memory_map : :class:`MemoryMap`
        Memory map of CSR registers.

    Interface attributes
    --------------------
    bus : :class:`Interface`
        CSR bus providing access to the contents of ``memory_map``.

    Raises
    ------
    :exc:`TypeError`
        If ``memory_map`` is not a :class:`MemoryMap` object.
    :exc:`ValueError`
        If ``memory_map`` has windows.
    :exc:`TypeError`
        If ``memory_map`` has resources that are not :class:`Register` objects.
    """
    def __init__(self, memory_map, byteorder="little"):
        if not isinstance(memory_map, MemoryMap):
            raise TypeError(f"CSR bridge memory map must be an instance of MemoryMap, not {memory_map!r}")
        if list(memory_map.windows()):
            raise ValueError("CSR bridge memory map cannot have windows")
        for reg, reg_name, (reg_start, reg_end) in memory_map.resources():
            if not isinstance(reg, Register):
                raise TypeError(f"CSR register must be an instance of csr.Register, not {reg!r}")
        if byteorder not in ("little", "big"):
            raise ValueError("Byte order must be either little or big")

        memory_map.freeze()
        self._mux = Multiplexer(memory_map, byteorder=byteorder)
        super().__init__({
            "bus": In(Signature(addr_width=memory_map.addr_width,
                                data_width=memory_map.data_width))
        })
        self.bus.memory_map = memory_map

    def elaborate(self, platform):
        m = Module()

        m.submodules.mux = self._mux
        for reg, reg_name, _ in self.bus.memory_map.resources():
            m.submodules["__".join(str(name) for name in reg_name)] = reg

        wiring.connect(m, flipped(self.bus), self._mux.bus)

        return m


class WishboneCSRBridge(wiring.Component):
    """Wishbone to CSR bridge.

    A bus bridge for accessing CSR registers from Wishbone. This bridge supports any Wishbone
    data width greater or equal to CSR data width and performs appropriate address translation.

    Latency
    -------

    Reads and writes always take ``self.data_width // csr_bus.data_width + 1`` cycles to complete,
    regardless of the select inputs. Write side effects occur simultaneously with acknowledgement.

    Parameters
    ----------
    csr_bus : :class:`..csr.Interface`
        CSR bus driven by the bridge.
    data_width : int
        Wishbone bus data width. Optional. If ``None``, defaults to ``csr_bus.data_width``.
    name : :class:`..memory.MemoryMap.Name`
        Window name. Optional.

    Attributes
    ----------
    wb_bus : :class:`..wishbone.Interface`
        Wishbone bus provided by the bridge.
    """
    def __init__(self, csr_bus, *, data_width=None, name=None, byteorder="little"):
        if isinstance(csr_bus, wiring.FlippedInterface):
            csr_bus_unflipped = flipped(csr_bus)
        else:
            csr_bus_unflipped = csr_bus
        if not isinstance(csr_bus_unflipped, Interface):
            raise TypeError(f"CSR bus must be an instance of csr.Interface, not "
                            f"{csr_bus_unflipped!r}")
        if csr_bus.data_width not in (8, 16, 32, 64):
            raise ValueError(f"CSR bus data width must be one of 8, 16, 32, 64, not "
                             f"{csr_bus.data_width!r}")
        if data_width is None:
            data_width = csr_bus.data_width
        if byteorder not in ("little", "big"):
            raise ValueError("Byte order must be either little or big")

        ratio  = data_width // csr_bus.data_width
        wb_sig = wishbone.Signature(addr_width=max(0, csr_bus.addr_width - exact_log2(ratio)),
                                    data_width=data_width,
                                    granularity=csr_bus.data_width)

        super().__init__({"wb_bus": In(wb_sig)})

        self.wb_bus.memory_map = MemoryMap(addr_width=csr_bus.addr_width,
                                           data_width=csr_bus.data_width)
        # Since granularity of the Wishbone interface matches the data width of the CSR bus,
        # no width conversion is performed, even if the Wishbone data width is greater.
        self.wb_bus.memory_map.add_window(csr_bus.memory_map, name=name)

        self._csr_bus = csr_bus
        self._byteorder = byteorder

    @property
    def csr_bus(self):
        return self._csr_bus

    def elaborate(self, platform):
        csr_bus = self.csr_bus
        wb_bus  = self.wb_bus

        m = Module()

        cycle = Signal(range(len(wb_bus.sel) + 1))
        m.d.comb += csr_bus.addr.eq(Cat(cycle[:exact_log2(len(wb_bus.sel))], wb_bus.adr))

        with m.If(wb_bus.cyc & wb_bus.stb):
            with m.Switch(cycle):
                def segment(index):
                    return slice(index * wb_bus.granularity, (index + 1) * wb_bus.granularity)

                for index in range(len(wb_bus.sel)):

                    if self._byteorder == "big":
                        curr_pos = len(wb_bus.sel) - index - 1
                        last_pos = curr_pos + 1
                    else:
                        curr_pos = index
                        last_pos = index - 1

                    sel_pos = wb_bus.sel[curr_pos]

                    with m.Case(index):
                        if index > 0:
                            # CSR reads are registered, and we need to re-register them.
                            m.d.sync += wb_bus.dat_r[segment(last_pos)].eq(csr_bus.r_data)
                        m.d.comb += csr_bus.r_stb.eq(sel_pos & ~wb_bus.we)
                        m.d.comb += csr_bus.w_data.eq(wb_bus.dat_w[segment(curr_pos)])
                        m.d.comb += csr_bus.w_stb.eq(sel_pos & wb_bus.we)
                        m.d.sync += cycle.eq(index + 1)

                with m.Default():
                    m.d.sync += wb_bus.dat_r[segment(curr_pos)].eq(csr_bus.r_data)
                    m.d.sync += wb_bus.ack.eq(1)

        with m.If(wb_bus.ack):
            m.d.sync += cycle.eq(0)
            m.d.sync += wb_bus.ack.eq(0)

        return m


class RWExtAction(csr.FieldAction):

    def __init__(self, shape):
        super().__init__(shape, access="rw", members={
            "r_data": In(shape),
            "r_stb":  Out(1),
            "w_data": Out(shape),
            "w_stb":  Out(1),
        })

    def elaborate(self, platform):
        m = Module()
        m.d.comb += [
            self.port.r_data.eq(self.r_data),
            self.r_stb.eq(self.port.r_stb),
            self.w_data.eq(self.port.w_data),
            self.w_stb.eq(self.port.w_stb),
        ]
        return m
