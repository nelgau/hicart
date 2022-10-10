from amaranth import *
from amaranth.sim import *
from amaranth_soc import wishbone

from hicart.interface.qspi_flash import QSPIBus, QSPIFlashWishboneInterface
from hicart.n64.ad16 import AD16
from hicart.n64.pi import PIWishboneInitiator
from hicart.soc.wishbone import DownConverter, Translator
from hicart.test.cocotb.harness import CocotbTestCase
from hicart.test.cocotb.driver.ad16 import PIBus, PIInitiator
from hicart.test.sim.qspi_clocker import QSPIClocker

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, FallingEdge


class DUT(Elaboratable):

    def __init__(self):
        self.ad16 = AD16()
        self.qspi = QSPIBus()

        self.flash_interface = QSPIFlashWishboneInterface()

        self.translator = Translator(sub_bus=self.flash_interface.bus,
                                        base_addr=0x800000,
                                        addr_width=24,
                                        features={"stall"})

        self.down_converter = DownConverter(sub_bus=self.translator.bus,
                                        addr_width=22,
                                        data_width=32,
                                        granularity=8,
                                        features={"stall"})

    def elaborate(self, platform):
        m = Module()

        # FIXME: Should the clocker be integrated into QSPIFlashInterface?
        clocker = QSPIClocker()
        initiator = PIWishboneInitiator()
        
        decoder = wishbone.Decoder(addr_width=32, data_width=32, granularity=8, features={"stall"})
        decoder.add(self.down_converter.bus, addr=0x10000000)

        m.submodules.initiator       = initiator
        m.submodules.clocker         = clocker
        m.submodules.decoder         = decoder
        m.submodules.flash_interface = self.flash_interface
        m.submodules.translator      = self.translator
        m.submodules.down_converter  = self.down_converter

        m.d.comb += [
            initiator.ad16              .connect( self.ad16 ),
            initiator.bus               .connect( decoder.bus ),
            self.flash_interface.qspi   .connect( clocker.qspi_in ),
            clocker.qspi_out            .connect( self.qspi )
        ]

        return m

    def ports(self):
        return [
            self.ad16.ad.i,
            self.ad16.ad.o,
            self.ad16.ad.oe,
            self.ad16.ale_h,
            self.ad16.ale_l,
            self.ad16.read,
            self.ad16.write,
            self.ad16.reset,

            self.qspi,
        ]


@cocotb.test()
async def run_CocotbTest_test_module(dut):
    dut.clk.setimmediatevalue(0)
    dut.rst.setimmediatevalue(0)

    dut.d__i.setimmediatevalue(0)

    clock = Clock(dut.clk, 16, units="ps")
    cocotb.start_soon(clock.start())

    pi_bus = PIBus.from_dut(dut)
    pi = PIInitiator(pi_bus)

    @cocotb.coroutine
    async def pi_process():
        await pi.begin()
        await pi.read_burst_fast(0x10000000, 256)

    await cocotb.start_soon(pi_process())

    for i in range(2):
        await FallingEdge(dut.clk)


class CocotbTest(CocotbTestCase):

    def test_module(self):
        dut = DUT()
        self.simulate(dut, traces=dut.ports())
