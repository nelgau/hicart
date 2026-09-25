from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth.utils import exact_log2
from amaranth_soc.memory import MemoryMap
from amaranth_soc import wishbone


class WindowMapper(wiring.Component):

    def __init__(self, sub_bus, *, addr_width, base_addr, name="mapped window"):
        if addr_width > sub_bus.addr_width:
            raise ValueError("Window mapper bus cannot be wider than subordinate bus")

        granularity_bits = exact_log2(sub_bus.data_width // sub_bus.granularity)
        effective_addr_width = addr_width + granularity_bits

        if base_addr & ((1 << effective_addr_width) - 1) != 0:
            raise ValueError("Window mapper bus cannot overlap base address")

        self.sub_bus = sub_bus
        self.base_addr = base_addr
        self._base_pattern = Const(self.base_addr >> effective_addr_width)

        # FIXME: It would be possible to implement this so that the resources
        # on the subordinate bus are visible, removing the need to create this
        # hacky placeholder resource. Unfortunately, because it's possible to
        # slice a resource using a window mapper, we'd need a way to represent
        # a subset of a resource and that doesn't seem trivial to do.
        map_addr_width = max(1, effective_addr_width)
        memory_map = MemoryMap(addr_width=map_addr_width, data_width=sub_bus.granularity)
        memory_map.add_resource(self, size=2**addr_width, name=name)

        bus_signature = wishbone.Signature(
            addr_width=addr_width,
            data_width=sub_bus.data_width,
            granularity=sub_bus.granularity,
            features=sub_bus.features)

        super().__init__({
            "bus": In(bus_signature)
        })
        self.bus.memory_map = memory_map

    def elaborate(self, platform):
        m = Module()

        m.d.comb += [
            self.sub_bus.adr    .eq(Cat(self.bus.adr, self._base_pattern)),

            self.sub_bus.dat_w  .eq(self.bus.dat_w),
            self.sub_bus.sel    .eq(self.bus.sel),
            self.sub_bus.cyc    .eq(self.bus.cyc),
            self.sub_bus.stb    .eq(self.bus.stb),
            self.sub_bus.we     .eq(self.bus.we),

            self.bus.dat_r      .eq(self.sub_bus.dat_r),
            self.bus.ack        .eq(self.sub_bus.ack),
        ]

        if hasattr(self.bus, "lock"):
            m.d.comb += self.sub_bus.lock.eq(self.bus.lock)
        if hasattr(self.bus, "cti"):
            m.d.comb += self.sub_bus.cti.eq(self.bus.cti)
        if hasattr(self.bus, "bte"):
            m.d.comb += self.sub_bus.bte.eq(self.bus.bte)
        if hasattr(self.bus, "err"):
            m.d.comb += self.bus.err.eq(self.sub_bus.err)
        if hasattr(self.bus, "rty"):
            m.d.comb += self.bus.rty.eq(self.sub_bus.rty)
        if hasattr(self.bus, "stall"):
            m.d.comb += self.bus.stall.eq(self.sub_bus.stall)

        return m
