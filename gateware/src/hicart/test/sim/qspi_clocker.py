from amaranth import *

from hicart.interface.qspi_flash import QSPIBus


class QSPIClocker(Elaboratable):

    def __init__(self):
        self.qspi_in = QSPIBus()
        self.qspi_out = QSPIBus()

    def elaborate(self, platform):
        m = Module()

        sync_clk = ClockSignal()

        m.d.comb += [
            self.qspi_out.sck   .eq(Mux(self.qspi_in.sck, ~sync_clk, 1)),
            self.qspi_out.cs_n  .eq(self.qspi_in.cs_n),

            self.qspi_in.d.i    .eq(self.qspi_out.d.i),
            self.qspi_out.d.o   .eq(self.qspi_in.d.o),
            self.qspi_out.d.oe  .eq(self.qspi_in.d.oe)
        ]

        return m
