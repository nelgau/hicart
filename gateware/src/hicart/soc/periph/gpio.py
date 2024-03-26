from amaranth import *
from amaranth import tracer
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth.utils import log2_int
from amaranth_soc import csr, wishbone
from amaranth_soc.csr.wishbone import WishboneCSRBridge
from amaranth_soc.memory import MemoryMap


class GPIOPeripheral(wiring.Component):
    def __init__(self, data_width=8, name=None, src_loc_at=1):
        if name is not None and not isinstance(name, str):
            raise TypeError("Name must be a string, not {!r}".format(name))
        self.name      = name or tracer.get_var_name(depth=1 + src_loc_at).lstrip("_")

        self.i = Signal(data_width)
        self.o = Signal(data_width)
        self.oe = Signal(data_width)

        self._i_csr   = csr.Element(data_width, csr.Element.Access.R)
        self._o_csr   = csr.Element(data_width, csr.Element.Access.RW)
        self._oe_csr  = csr.Element(data_width, csr.Element.Access.RW)

        self._csr_mux = csr.Multiplexer(addr_width=4, data_width=8, alignment=2)
        self._csr_mux.add(self._i_csr, name="i", alignment=2)
        self._csr_mux.add(self._o_csr, name="o", alignment=2)
        self._csr_mux.add(self._oe_csr, name="oe", alignment=2)

        self._csr_bridge = WishboneCSRBridge(self._csr_mux.bus, data_width=32)

        wb_signature = wishbone.Signature(
            addr_width=self._csr_bridge.wb_bus.addr_width,
            data_width=self._csr_bridge.wb_bus.data_width,
            granularity=self._csr_bridge.wb_bus.granularity)

        memory_map = MemoryMap(addr_width=self._csr_mux.bus.addr_width,
                               data_width=self._csr_mux.bus.data_width)
        memory_map.add_window(self._csr_bridge.wb_bus.memory_map)

        super().__init__(
            {"bus": In(wb_signature)
        })
        self.bus.memory_map = memory_map

    def elaborate(self, platform):
        m = Module()

        m.submodules.csr_mux = self._csr_mux
        m.submodules.csr_bridge = self._csr_bridge

        wiring.connect(m, wiring.flipped(self.bus), self._csr_bridge.wb_bus)

        m.d.comb += [
            self._i_csr.r_data.eq(self.i),
            self._o_csr.r_data.eq(self.o),
            self._oe_csr.r_data.eq(self.oe)
        ]

        with m.If(self._o_csr.w_stb):
            m.d.sync += self.o.eq(self._o_csr.w_data)

        with m.If(self._oe_csr.w_stb):
            m.d.sync += self.oe.eq(self._oe_csr.w_data)

        return m
