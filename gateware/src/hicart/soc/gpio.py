from amaranth import *
from lambdasoc.periph.base import Peripheral


class GPIOPeripheral(Peripheral, Elaboratable):
    def __init__(self, data_width=8):
        super().__init__()

        self.i = Signal(data_width)
        self.o = Signal(data_width)
        self.oe = Signal(data_width)

        bank          = self.csr_bank()
        self._i_csr   = bank.csr(data_width, "r")
        self._o_csr   = bank.csr(data_width, "rw")
        self._oe_csr  = bank.csr(data_width, "rw")

        self._bridge  = self.bridge(data_width=32, granularity=8, alignment=2)
        self.bus      = self._bridge.bus      

    def elaborate(self, platform):
        m = Module()
        m.submodules.bridge = self._bridge

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
