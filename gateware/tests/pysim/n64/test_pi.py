from amaranth import *
from amaranth.sim import *
from amaranth_soc import wishbone
from lambdasoc.periph.sram  import SRAMPeripheral

from hicart.n64.ad16 import AD16
from hicart.n64.pi import PIWishboneInitiator
from hicart.test.pysim.utils import ModuleTestCase, sync_test_case


class PIWishboneInitiatorTest(ModuleTestCase):

    class DUT(Elaboratable):

        def __init__(self):
            self.ad16 = AD16()

            self.rom_data = [
                0x76543210,
                0xFEDCBA98,
                0xCAFEBABE,
                0xDEADBEEF,
            ]

        def elaborate(self, platform):
            m = Module()

            self.decoder = wishbone.Decoder(addr_width=30, data_width=32, granularity=8, features={"stall"})

            self.rom = SRAMPeripheral(size=16, data_width=32, writable=False)
            self.decoder.add(self.rom.bus, addr=0x10000000)
            self.rom.init = self.rom_data

            self.initiator = PIWishboneInitiator()

            m.submodules.initiator = self.initiator
            m.submodules.decoder   = self.decoder
            m.submodules.rom       = self.rom

            m.d.comb += [
                self.initiator.ad16 .connect( self.ad16 ),
                self.initiator.bus  .connect( self.decoder.bus ),
            ]

            return m

    FRAGMENT_UNDER_TEST = DUT

    def traces_of_interest(self):
        return [
            self.dut.ad16.ad.i,
            self.dut.ad16.ad.o,
            self.dut.ad16.ad.oe,
            self.dut.ad16.ale_h,
            self.dut.ad16.ale_l,
            self.dut.ad16.read,
            self.dut.ad16.write,
            self.dut.ad16.reset
        ]        

    @sync_test_case
    def test_basic(self):
        # Ale_l is active in idle state
        yield self.dut.ad16.ale_l   .eq(1)
        yield from self.advance_cycles(2)

        # Latch address

        yield self.dut.ad16.ale_l   .eq(0)
        yield self.dut.ad16.ad.i    .eq(0x1000)
        yield
        yield self.dut.ad16.ale_h   .eq(1)
        yield self.dut.ad16.ad.i    .eq(0x0002)
        yield
        yield self.dut.ad16.ale_l   .eq(1)
        yield from self.advance_cycles(8)

        #

        for i in range(8):

            yield self.dut.ad16.read   .eq(1)
            yield from self.advance_cycles(6)
            yield self.dut.ad16.read   .eq(0)
            yield from self.advance_cycles(6)
