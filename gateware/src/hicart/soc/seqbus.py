from contextlib import contextmanager

from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.fifo import SyncFIFOBuffered
from amaranth.lib.wiring import In, Out, flipped
from amaranth.utils import exact_log2
from amaranth_soc import wishbone
from amaranth_soc.memory import MemoryMap

from hicart.soc.wishbone import WishboneFeatureShim


class Signature(wiring.Signature):
    """Seqbus interface signature.

    Similar to classic non-pipelined Wishbone with an additional constraint:

        - During a cycle, ADR is always valid and increments after ACK.

    """
    def __init__(self, addr_width, data_width, granularity=None):
        if granularity is None:
            granularity = data_width

        if not isinstance(addr_width, int) or addr_width < 0:
            raise TypeError(f"Address width must be a non-negative integer, not {addr_width!r}")
        if data_width not in (8, 16, 32, 64):
            raise ValueError(f"Data width must be one of 8, 16, 32, 64, not {data_width!r}")
        if granularity not in (8, 16, 32, 64):
            raise ValueError(f"Granularity must be one of 8, 16, 32, 64, not {granularity!r}")
        if granularity > data_width:
            raise ValueError(f"Granularity {granularity} may not be greater than data width "
                             f"{data_width}")

        self._addr_width  = addr_width
        self._data_width  = data_width
        self._granularity = granularity

        super().__init__({
            "adr":      Out(self.addr_width),
            "dat_r":    In(self.data_width),
            "dat_w":    Out(self.data_width),
            "sel":      Out(self.data_width // self.granularity),
            "cyc":      Out(1),
            "stb":      Out(1),
            "we":       Out(1),
            "ack":      In(1),
            "err":      In(1),
        })

    @property
    def addr_width(self):
        return self._addr_width

    @property
    def data_width(self):
        return self._data_width

    @property
    def granularity(self):
        return self._granularity

    def create(self, *, path=None, src_loc_at=0):
        return Interface(addr_width=self.addr_width, data_width=self.data_width,
                         granularity=self.granularity, path=path, src_loc_at=1 + src_loc_at)

    def __eq__(self, other):
        return (isinstance(other, Signature) and
                self.addr_width == other.addr_width and
                self.data_width == other.data_width and
                self.granularity == other.granularity)

    def __repr__(self):
        return f"seqbus.Signature({self.members!r})"


class Interface(wiring.PureInterface):

    def __init__(self, *, addr_width, data_width, granularity=None, path=None, src_loc_at=0):
        super().__init__(Signature(addr_width=addr_width, data_width=data_width,
                                    granularity=granularity),
                         path=path, src_loc_at=1 + src_loc_at)
        self._memory_map = None

    @property
    def addr_width(self):
        return self.signature.addr_width

    @property
    def data_width(self):
        return self.signature.data_width

    @property
    def granularity(self):
        return self.signature.granularity

    @property
    def memory_map(self):
        if self._memory_map is None:
            raise AttributeError(f"{self!r} does not have a memory map")
        return self._memory_map

    @memory_map.setter
    def memory_map(self, memory_map):
        if not isinstance(memory_map, MemoryMap):
            raise TypeError(f"Memory map must be an instance of MemoryMap, not {memory_map!r}")
        if memory_map.data_width != self.granularity:
            raise ValueError(f"Memory map has data width {memory_map.data_width}, which is "
                             f"not the same as bus interface granularity {self.granularity}")
        granularity_bits = exact_log2(self.data_width // self.granularity)
        effective_addr_width = self.addr_width + granularity_bits
        if memory_map.addr_width != max(1, effective_addr_width):
            raise ValueError(f"Memory map has address width {memory_map.addr_width}, which is "
                             f"not the same as the bus interface effective address width "
                             f"{effective_addr_width} (= {self.addr_width} address bits + "
                             f"{granularity_bits} granularity bits)")
        self._memory_map = memory_map

    def __repr__(self):
        return f"seqbus.Interface({self.signature!r})"


class Decoder(wiring.Component):

    def __init__(self, *, addr_width, data_width, granularity=None, alignment=0, name=None):
        if granularity is None:
            granularity = data_width
        super().__init__({"bus": In(Signature(addr_width=addr_width, data_width=data_width,
                                              granularity=granularity))})
        granularity_bits = exact_log2(data_width // granularity)
        effective_addr_width = addr_width + granularity_bits
        self.bus.memory_map = MemoryMap(addr_width=max(1, effective_addr_width),
                                        data_width=granularity, alignment=alignment)
        self._subs = dict()

    def align_to(self, alignment):
        return self.bus.memory_map.align_to(alignment)

    def add(self, sub_bus, *, name=None, addr=None, sparse=False):
        if isinstance(sub_bus, wiring.FlippedInterface):
            sub_bus_unflipped = flipped(sub_bus)
        else:
            sub_bus_unflipped = sub_bus
        if not isinstance(sub_bus_unflipped, Interface):
            raise TypeError(f"Subordinate bus must be an instance of wishbone.Interface, not "
                            f"{sub_bus_unflipped!r}")
        if sub_bus.granularity > self.bus.granularity:
            raise ValueError(f"Subordinate bus has granularity {sub_bus.granularity}, which is "
                             f"greater than the decoder granularity {self.bus.granularity}")
        if not sparse:
            if sub_bus.data_width != self.bus.data_width:
                raise ValueError(f"Subordinate bus has data width {sub_bus.data_width}, which is "
                                 f"not the same as decoder data width {self.bus.data_width} "
                                 f"(required for dense address translation)")
        else:
            if sub_bus.granularity != sub_bus.data_width:
                raise ValueError(f"Subordinate bus has data width {sub_bus.data_width}, which is "
                                 f"not the same as its granularity {sub_bus.granularity} "
                                 f"(required for sparse address translation)")

        self._subs[sub_bus.memory_map] = sub_bus
        return self.bus.memory_map.add_window(sub_bus.memory_map, name=name, addr=addr,
                                              sparse=sparse)

    def elaborate(self, platform):
        m = Module()

        matched = Signal()
        sub_err = Signal()

        with m.Switch(self.bus.adr):
            for sub_map, sub_name, (sub_pattern, ratio) in self.bus.memory_map.window_patterns():
                sub_bus = self._subs[sub_map]

                m.d.comb += [
                    sub_bus.adr.eq(self.bus.adr << exact_log2(ratio)),
                    sub_bus.dat_w.eq(self.bus.dat_w),
                    sub_bus.sel.eq(Cat(sel.replicate(ratio) for sel in self.bus.sel)),
                    sub_bus.we.eq(self.bus.we),
                    sub_bus.stb.eq(self.bus.stb),
                ]

                granularity_bits = exact_log2(self.bus.data_width // self.bus.granularity)
                with m.Case(sub_pattern[:-granularity_bits if granularity_bits > 0 else None]):
                    m.d.comb += [
                        sub_bus.cyc.eq(self.bus.cyc),
                        self.bus.dat_r.eq(sub_bus.dat_r),
                        self.bus.ack.eq(sub_bus.ack),
                        sub_err.eq(sub_bus.err),
                        matched.eq(1),
                    ]

        m.d.comb += self.bus.err.eq(self.bus.stb & Mux(matched, sub_err, 1))

        return m


class WishboneBridge(wiring.Component):

    def __init__(self, wb):
        self.wb = wb

        super().__init__({
            "seq": In(Signature(addr_width=wb.addr_width,
                                data_width=wb.data_width,
                                granularity=wb.granularity)),
        })
        granularity_bits = exact_log2(wb.data_width // wb.granularity)
        effective_addr_width = wb.addr_width + granularity_bits
        self.seq.memory_map = MemoryMap(addr_width=max(1, effective_addr_width),
                                        data_width=wb.granularity)
        self.seq.memory_map.add_window(wb.memory_map)
        self.seq.memory_map.freeze()

    def elaborate(self, platform):
        m = Module()

        shim = WishboneFeatureShim(self.wb.addr_width, self.wb.data_width,
                                   self.wb.granularity, intr_features=frozenset(),
                                   sub_features=self.wb.features)
        m.submodules.shim = shim

        wiring.connect(m, shim.sub_bus, self.wb)

        m.d.comb += [
            shim.intr_bus.adr.eq(self.seq.adr),
            shim.intr_bus.dat_w.eq(self.seq.dat_w),
            shim.intr_bus.sel.eq(self.seq.sel),
            shim.intr_bus.cyc.eq(self.seq.cyc),
            shim.intr_bus.stb.eq(self.seq.stb),
            shim.intr_bus.we.eq(self.seq.we),

            self.seq.dat_r.eq(shim.intr_bus.dat_r),
            self.seq.ack.eq(shim.intr_bus.ack),
        ]

        return m

class PrefetchingWishboneBridge(wiring.Component):
    """Bridge from Seq to Wishbone that prefetches as soon as the cycle begins.

    This component silently discards writes.
    """
    def __init__(self, wb, depth=4):
        self.wb = wb
        self.depth = depth

        super().__init__({
            "seq": In(Signature(addr_width=wb.addr_width,
                                data_width=wb.data_width,
                                granularity=wb.granularity)),
        })
        granularity_bits = exact_log2(wb.data_width // wb.granularity)
        effective_addr_width = wb.addr_width + granularity_bits
        self.seq.memory_map = MemoryMap(addr_width=max(1, effective_addr_width),
                                        data_width=wb.granularity)
        self.seq.memory_map.add_window(wb.memory_map)
        self.seq.memory_map.freeze()

    def elaborate(self, platform):
        m = Module()

        shim = WishboneFeatureShim(self.wb.addr_width, self.wb.data_width,
                                   self.wb.granularity, intr_features=frozenset(),
                                   sub_features=self.wb.features)
        m.submodules.shim = shim

        wiring.connect(m, shim.sub_bus, self.wb)

        read_fifo_reset = Signal()
        read_enabled = Signal()
        read_address = Signal(32)

        read_fifo = SyncFIFOBuffered(width=self.wb.data_width, depth=self.depth)
        read_fifo = ResetInserter(read_fifo_reset)(read_fifo)
        m.submodules.read_fifo = read_fifo

        # Seq

        m.d.comb += read_fifo_reset.eq(~self.seq.cyc)

        with m.If(self.seq.cyc):
            with m.If(~read_enabled):
                m.d.sync += read_address.eq(self.seq.adr)
                m.d.sync += read_enabled.eq(1)
        with m.Else():
            m.d.sync += read_enabled.eq(0)

        # Writes also consume from the read fifo to keep it consistent
        with m.If(~self.seq.ack & self.seq.stb):
            with m.If(read_fifo.r_rdy):
                m.d.sync += self.seq.dat_r.eq(read_fifo.r_data)
                m.d.sync += self.seq.ack.eq(1)
                m.d.sync += read_fifo.r_en.eq(1)

        with m.If(self.seq.ack):
            m.d.sync += self.seq.ack.eq(0)
            m.d.sync += read_fifo.r_en.eq(0)

        # Wishbone

        with m.If(read_enabled & ~shim.intr_bus.cyc):
            with m.If(read_fifo.w_rdy):
                m.d.sync += shim.intr_bus.adr.eq(read_address),
                m.d.sync += shim.intr_bus.cyc.eq(1)
                m.d.sync += shim.intr_bus.stb.eq(1)
                m.d.sync += shim.intr_bus.we.eq(0)

        with m.If(self.wb.ack):
            m.d.sync += shim.intr_bus.cyc.eq(0)
            m.d.sync += shim.intr_bus.stb.eq(0)
            m.d.sync += read_address.eq(read_address + 1)

        m.d.comb += [
            read_fifo.w_en.eq(self.wb.ack),
            read_fifo.w_data.eq(self.wb.dat_r),
        ]

        return m


class DriverBusError(Exception):
    pass


class SeqbusDriver:

    def __init__(self, bus):
        self.bus = bus

    async def begin(self, ctx):
        pass

    async def read_once(self, ctx, address, initial_delay=0):
        ctx.set(self.bus.adr, address)
        ctx.set(self.bus.cyc, 1)

        for _ in range(initial_delay):
            await ctx.tick()

        ctx.set(self.bus.stb, 1)
        await ctx.tick()

        while not ctx.get(self.bus.ack | self.bus.err):
            await ctx.tick()

        if ctx.get(self.bus.err):
            raise DriverBusError()

        result = ctx.get(self.bus.dat_r)
        await ctx.tick()

        ctx.set(self.bus.cyc, 0)
        ctx.set(self.bus.stb, 0)
        await ctx.tick()

        return result

    async def read_sequential(self, ctx, start_address, count, initial_delay=0, delay=0):
        current_address = start_address
        result = []

        ctx.set(self.bus.adr, current_address)
        ctx.set(self.bus.cyc, 1)

        for _ in range(initial_delay):
            await ctx.tick()

        for i in range(count):
            ctx.set(self.bus.stb, 1)
            await ctx.tick()

            while not ctx.get(self.bus.ack | self.bus.err):
                await ctx.tick()

            if ctx.get(self.bus.err):
                raise DriverBusError()

            result.append(ctx.get(self.bus.dat_r))
            await ctx.tick()

            current_address += 1
            ctx.set(self.bus.adr, current_address)

            if delay > 0 and i < count - 1:
                ctx.set(self.bus.stb, 0)
                for _ in range(delay):
                    await ctx.tick()

        ctx.set(self.bus.adr, 0)
        ctx.set(self.bus.cyc, 0)
        ctx.set(self.bus.stb, 0)
        await ctx.tick()

        return result

    async def write_once(self, ctx, address, data, initial_delay=0):
        ctx.set(self.bus.adr, address)
        ctx.set(self.bus.cyc, 1)

        for _ in range(initial_delay):
            await ctx.tick()

        sel = C(1).replicate(len(self.bus.sel))

        ctx.set(self.bus.stb, 1)
        ctx.set(self.bus.we, 1)
        ctx.set(self.bus.sel, sel)
        ctx.set(self.bus.dat_w, data)
        await ctx.tick()

        while not ctx.get(self.bus.ack):
            await ctx.tick()

        await ctx.tick()

        ctx.set(self.bus.cyc, 0)
        ctx.set(self.bus.stb, 0)
        ctx.set(self.bus.we, 0)
        ctx.set(self.bus.sel, 0)
        ctx.set(self.bus.dat_w, 0)
        await ctx.tick()


class SeqbusResponder:

    def __init__(self, bus, *, initial=0, delay=0):
        if delay < 0:
            raise ValueError(f"Delay must be non-negative")

        self.bus = bus
        self.delay = delay
        self.counter = initial

    async def run(self, ctx):
        ctx.set(self.bus.ack, 0)
        ctx.set(self.bus.dat_r, 0)

        expected_address = None

        while True:
            _, rst_active, cyc, stb, adr, we, dat_w = await (
                ctx.tick().sample(
                    self.bus.cyc,
                    self.bus.stb,
                    self.bus.adr,
                    self.bus.we,
                    self.bus.dat_w))

            if rst_active or not cyc:
                expected_address = None
                continue

            if cyc and expected_address is None:
                expected_address = adr

            if cyc & stb:
                assert adr == expected_address

                for _ in range(self.delay):
                    await ctx.tick()

                result = 0

                if we:
                    self.counter = dat_w
                else:
                    result = self.counter
                    self.counter += 1

                ctx.set(self.bus.ack, 1)
                ctx.set(self.bus.dat_r, result)

                expected_address += 1

                await ctx.tick()

                ctx.set(self.bus.ack, 0)
                ctx.set(self.bus.dat_r, 0)
