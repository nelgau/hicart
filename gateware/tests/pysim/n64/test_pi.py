from amaranth import *
from amaranth.lib import wiring
from amaranth.sim import *
from amaranth_soc import wishbone
from hicart.soc.periph.sram  import SRAMPeripheral

from hicart.n64.cartbus import PISignature
from hicart.n64.pi import WishboneBridge
from hicart.test.pysim.utils import ModuleTestCase, sync_test_case


class WishboneBridgeTest(ModuleTestCase):

    class DUT(Elaboratable):

        def __init__(self):
            self.pi = PISignature.create()

            self.rom_data = [
                0x3210,
                0xBA98,
                0xBABE,
                0xBEEF,
            ]

        def elaborate(self, platform):
            m = Module()

            self.decoder = wishbone.Decoder(addr_width=31, data_width=16, granularity=8, features={"stall"})

            self.rom = SRAMPeripheral(size=16, data_width=16, writable=False)
            self.decoder.add(self.rom.bus, addr=0x10000000)
            self.rom.init = self.rom_data

            self.initiator = WishboneBridge()

            m.submodules.initiator = self.initiator
            m.submodules.decoder   = self.decoder
            m.submodules.rom       = self.rom

            wiring.connect(m, self.initiator.pi, wiring.flipped(self.pi))
            wiring.connect(m, self.initiator.wb, self.decoder.bus)

            return m

    FRAGMENT_UNDER_TEST = DUT

    def traces_of_interest(self):
        return [
            self.dut.pi.ad.i,
            self.dut.pi.ad.o,
            self.dut.pi.ad.oe,
            self.dut.pi.ale_h.i,
            self.dut.pi.ale_l.i,
            self.dut.pi.read.i,
            self.dut.pi.write.i
        ]        

    @sync_test_case
    def test_basic(self):
        # Ale_l is active in idle state
        yield self.dut.pi.ale_l.i.eq(1)
        yield self.dut.pi.ale_h.i.eq(0)
        yield from self.advance_cycles(6)

        # Latch address

        yield self.dut.pi.ale_l.i   .eq(0)
        yield from self.advance_cycles(2)
        yield self.dut.pi.ad.i      .eq(0x1000)
        yield from self.advance_cycles(2)
        yield self.dut.pi.ale_h.i   .eq(1)
        yield from self.advance_cycles(2)
        yield self.dut.pi.ad.i      .eq(0x0002)
        yield from self.advance_cycles(2)
        yield self.dut.pi.ale_l.i   .eq(1)
        yield from self.advance_cycles(8)

        # Read

        for i in range(3):

            yield self.dut.pi.read.i    .eq(1)
            yield from self.advance_cycles(6)
            yield self.dut.pi.read.i    .eq(0)
            yield from self.advance_cycles(6)
