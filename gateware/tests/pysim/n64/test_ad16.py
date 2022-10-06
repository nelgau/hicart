from amaranth import *
from amaranth.sim import *

from hicart.n64.ad16 import AD16Interface
from hicart.test.pysim.utils import ModuleTestCase, sync_test_case


class AD16InterfaceTest(ModuleTestCase):
    FRAGMENT_UNDER_TEST = AD16Interface

    def traces_of_interest(self):
        return [
            self.dut.bus.blk,
            self.dut.bus.base,
            self.dut.bus.load,
            self.dut.bus.blk_stall,
            self.dut.bus.off,
            self.dut.bus.dat_w,
            self.dut.bus.dat_r,
            self.dut.bus.cyc,
            self.dut.bus.stb,
            self.dut.bus.we,
            self.dut.bus.stall,
            self.dut.bus.ack,

            self.dut.ad16.ad.i,
            self.dut.ad16.ad.o,
            self.dut.ad16.ad.oe,
            self.dut.ad16.ale_h,
            self.dut.ad16.ale_l,
            self.dut.ad16.read,
            self.dut.ad16.write,
            self.dut.ad16.reset
        ]

    def initialize_signals(self):
        yield self.dut.ad16.ad.i    .eq(0)
        yield self.dut.ad16.ale_h   .eq(0)
        yield self.dut.ad16.ale_l   .eq(0)
        yield self.dut.ad16.read    .eq(0)
        yield self.dut.ad16.write   .eq(0)
        yield self.dut.ad16.reset   .eq(0)

    @sync_test_case
    def test_basic(self):
        yield self.dut.bus.blk_stall.eq(1)
        yield from self.advance_cycles(2)

        # Ale_l is active in idle state
        yield self.dut.ad16.ale_l   .eq(1)
        yield from self.advance_cycles(4)

        # Latch address

        yield self.dut.ad16.ale_l   .eq(0)
        yield from self.advance_cycles(6)

        yield self.dut.ad16.ad.i    .eq(0x8765)
        yield from self.advance_cycles(6)

        yield self.dut.ad16.ale_h   .eq(1)
        yield from self.advance_cycles(6)

        yield self.dut.ad16.ad.i    .eq(0x4321)
        yield from self.advance_cycles(6)

        yield self.dut.ad16.ale_l   .eq(1)
        yield from self.advance_cycles(6)

        yield self.dut.ad16.ad.i    .eq(0)
        yield from self.advance_cycles(6)

        # 

        self.assertEqual((yield self.dut.bus.blk),  1)
        self.assertEqual((yield self.dut.bus.base), 0x21D950C8)
        self.assertEqual((yield self.dut.bus.load), 1)

        yield

        self.assertEqual((yield self.dut.bus.load), 1)

        yield self.dut.bus.blk_stall.eq(0)
        yield
        yield

        self.assertEqual((yield self.dut.bus.load), 0)




        #

        yield from self.advance_cycles(2)

        yield self.dut.ad16.read   .eq(1)
        yield from self.advance_cycles(6)

        #

        yield self.dut.bus.dat_r.eq(0xCAFEBABE)
        yield self.dut.bus.ack.eq(1)
        yield

        yield self.dut.bus.ack.eq(0)
        yield self.dut.bus.dat_r.eq(0)
        yield
        yield

        self.assertEqual((yield self.dut.ad16.ad.o),  0xCAFE)
        self.assertEqual((yield self.dut.ad16.ad.oe), 1)

        #

        yield self.dut.ad16.read   .eq(0)
        yield

        yield from self.advance_cycles(3)

        self.assertEqual((yield self.dut.ad16.ad.oe), 0)

        #

        yield from self.advance_cycles(2)

        yield self.dut.ad16.read   .eq(1)
        yield from self.advance_cycles(6)
  
        self.assertEqual((yield self.dut.ad16.ad.o),  0xBABE)
        self.assertEqual((yield self.dut.ad16.ad.oe), 1)

        #

        yield self.dut.ad16.read   .eq(0)
        yield

        yield from self.advance_cycles(3)

        self.assertEqual((yield self.dut.ad16.ad.oe), 0)






        #

        yield from self.advance_cycles(2)

        yield self.dut.ad16.read   .eq(1)
        yield from self.advance_cycles(6)

        #

        yield self.dut.bus.dat_r.eq(0xDEADBEEF)
        yield self.dut.bus.ack.eq(1)
        yield

        yield self.dut.bus.ack.eq(0)
        yield self.dut.bus.dat_r.eq(0)
        yield        
        yield

        self.assertEqual((yield self.dut.ad16.ad.o),  0xDEAD)
        self.assertEqual((yield self.dut.ad16.ad.oe), 1)

        #

        yield self.dut.ad16.read   .eq(0)
        yield

        yield from self.advance_cycles(3)

        self.assertEqual((yield self.dut.ad16.ad.oe), 0)

        #

        yield from self.advance_cycles(2)

        yield self.dut.ad16.read   .eq(1)
        yield from self.advance_cycles(6)
  
        self.assertEqual((yield self.dut.ad16.ad.o),  0xBEEF)
        self.assertEqual((yield self.dut.ad16.ad.oe), 1)

        #

        yield self.dut.ad16.read   .eq(0)
        yield

        yield from self.advance_cycles(3)

        self.assertEqual((yield self.dut.ad16.ad.oe), 0)




        #

        yield self.dut.ad16.ale_h   .eq(0)
        yield

        yield from self.advance_cycles(4)

        self.assertEqual((yield self.dut.bus.blk),  0)
