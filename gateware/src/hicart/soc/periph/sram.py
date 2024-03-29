from amaranth import *
from amaranth import tracer
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth.utils import exact_log2

from amaranth_soc import wishbone
from amaranth_soc.memory import MemoryMap
from amaranth_soc.periph import ConstantMap


__all__ = ["SRAMPeripheral"]


class SRAMPeripheral(wiring.Component):
    """SRAM storage peripheral.

    Parameters
    ----------
    size : int
        Memory size in bytes.
    data_width : int
        Bus data width.
    granularity : int
        Bus granularity.
    writable : bool
        Memory is writable.

    Attributes
    ----------
    bus : :class:`amaranth_soc.wishbone.Interface`
        Wishbone bus interface.
    """
    # TODO raise bus.err if read-only and a bus write is attempted.
    def __init__(self, *, size, data_width=32, granularity=8, writable=True, init=None, name="sram", src_loc_at=1):
        if name is not None and not isinstance(name, str):
            raise TypeError("Name must be a string, not {!r}".format(name))
        self.name = name or tracer.get_var_name(depth=1 + src_loc_at).lstrip("_")

        if not isinstance(size, int) or size <= 0 or size & size-1:
            raise ValueError("Size must be an integer power of two, not {!r}"
                             .format(size))
        if size < data_width // granularity:
            raise ValueError("Size {} cannot be lesser than the data width/granularity ratio "
                             "of {} ({} / {})"
                              .format(size, data_width // granularity, data_width, granularity))

        self._mem = Memory(depth=(size * granularity) // data_width, width=data_width, init=init)

        bus_signature = wishbone.Signature(addr_width=exact_log2(self._mem.depth),
                                           data_width=self._mem.width, granularity=granularity,
                                           features={"cti", "bte"})

        memory_map = MemoryMap(addr_width=exact_log2(size), data_width=granularity, name=self.name)
        memory_map.add_resource(self._mem, name="mem", size=size)

        self.size        = size
        self.granularity = granularity
        self.writable    = writable

        super().__init__({
            "bus": In(bus_signature)
        })
        self.bus.memory_map = memory_map

    @property
    def signature(self):
        return self._signature

    @property
    def init(self):
        return self._mem.init

    @init.setter
    def init(self, init):
        self._mem.init = init

    @property
    def constant_map(self):
        return ConstantMap(
            SIZE = self.size,
        )

    def elaborate(self, platform):
        m = Module()

        incr = Signal.like(self.bus.adr)

        with m.Switch(self.bus.bte):
            with m.Case(wishbone.BurstTypeExt.LINEAR):
                m.d.comb += incr.eq(self.bus.adr + 1)
            with m.Case(wishbone.BurstTypeExt.WRAP_4):
                m.d.comb += incr[:2].eq(self.bus.adr[:2] + 1)
                m.d.comb += incr[2:].eq(self.bus.adr[2:])
            with m.Case(wishbone.BurstTypeExt.WRAP_8):
                m.d.comb += incr[:3].eq(self.bus.adr[:3] + 1)
                m.d.comb += incr[3:].eq(self.bus.adr[3:])
            with m.Case(wishbone.BurstTypeExt.WRAP_16):
                m.d.comb += incr[:4].eq(self.bus.adr[:4] + 1)
                m.d.comb += incr[4:].eq(self.bus.adr[4:])

        m.submodules.mem_rp = mem_rp = self._mem.read_port()
        m.d.comb += self.bus.dat_r.eq(mem_rp.data)

        with m.If(self.bus.ack):
            m.d.sync += self.bus.ack.eq(0)

        with m.If(self.bus.cyc & self.bus.stb):
            m.d.sync += self.bus.ack.eq(1)
            with m.If((self.bus.cti == wishbone.CycleType.INCR_BURST) & self.bus.ack):
                m.d.comb += mem_rp.addr.eq(incr)
            with m.Else():
                m.d.comb += mem_rp.addr.eq(self.bus.adr)

        if self.writable:
            m.submodules.mem_wp = mem_wp = self._mem.write_port(granularity=self.granularity)
            m.d.comb += mem_wp.addr.eq(mem_rp.addr)
            m.d.comb += mem_wp.data.eq(self.bus.dat_w)
            with m.If(self.bus.cyc & self.bus.stb & self.bus.we):
                m.d.comb += mem_wp.en.eq(self.bus.sel)

        return m
