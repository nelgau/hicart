from amaranth import *
from amaranth_soc import wishbone
import cocotb
import pytest

from hicart.interface.qspi_flash import QSPIFlashWishboneInterface
from hicart.n64.pi import WishboneBridge
from hicart.platforms.homeinvader_rev_a import HomeInvaderRevAPlatform
from hicart.soc.wishbone import DownConverter, Translator
from hicart.test.cocotb import Accessor, CocotbTestCase, init_domains, start_clock, do_reset
from hicart.test.cocotb.driver.ad16 import PIInitiator
from hicart.test.cocotb.emulator.qspi_flash import QSPIFlashEmulator
from hicart.test.sim.qspi_clocker import QSPIClocker


class DUT(Elaboratable):

    def __init__(self):
        from hicart.n64.ad16 import AD16
        from hicart.interface.qspi_flash import QSPIBus

        self.ad16 = AD16(name='ad16')
        self.qspi = QSPIBus(name='qspi')

        self.flash_interface = QSPIFlashWishboneInterface()

        self.translator = Translator(sub_bus=self.flash_interface.bus,
                                        base_addr=0x800000,
                                        addr_width=24,
                                        features={"stall"})

        self.down_converter = DownConverter(sub_bus=self.translator.bus,
                                        addr_width=23,
                                        data_width=16,
                                        granularity=8,
                                        features={"stall"})

    def elaborate(self, platform):
        m = Module()

        # FIXME: Should the clocker be integrated into QSPIFlashInterface?
        clocker = QSPIClocker()
        initiator = WishboneBridge()
        
        decoder = wishbone.Decoder(addr_width=31, data_width=16, granularity=8, features={"stall"})
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
            self.ad16,
            self.qspi,
        ]


@cocotb.test()
async def run_CocotbTest_test_module(dut):
    from hicart.n64.ad16 import ad16_layout
    from hicart.interface.qspi_flash import qspi_layout

    ad16_accessor = Accessor.from_layout(ad16_layout)
    qspi_accessor = Accessor.from_layout(qspi_layout)

    ad16 = ad16_accessor(dut, name='ad16')
    qspi = qspi_accessor(dut, name='qspi')

    pi = PIInitiator(ad16)
    flash = QSPIFlashEmulator(qspi)

    await pi.begin()
    await flash.begin()

    init_domains(dut)
    start_clock(dut.clk, rate=60e6)
    await do_reset(dut)

    @cocotb.coroutine
    async def pi_process():
        await pi.read_burst_fast(0x10000000, 256)

    await cocotb.start_soon(pi_process())


@pytest.mark.skip(reason="Needs to be rewriten to use lib.wiring")
class CocotbTest(CocotbTestCase):
    def test_module(self):
        dut = DUT()
        platform = HomeInvaderRevAPlatform()
        self.simulate(dut, traces=dut.ports(), platform=platform)
