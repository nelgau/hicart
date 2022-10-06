from amaranth import *
from amaranth.sim import *

from hicart.n64.burst import BufferedBurst2Wishbone
from hicart.test.testcase import MultiProcessTestCase


class BufferedBurst2WishboneTest(MultiProcessTestCase):

    def test_basic(self):
        dut = BufferedBurst2Wishbone()

        def bbus_process():
            yield

            yield dut.bbus.blk          .eq(1)
            yield dut.bbus.load         .eq(1)
            yield dut.bbus.base         .eq(0x1000)
            yield

            yield dut.bbus.load         .eq(0)
            yield

            for i in range(20):
                yield

            yield dut.bbus.blk          .eq(0)

            for i in range(20):
                yield            

        def wbbus_process():
            yield Passive()

            data = 0xCAFEBA00

            while True:
                while (yield ~(dut.wbbus.cyc & dut.wbbus.stb)):
                    yield

                yield
                yield dut.wbbus.stall       .eq(1)

                yield
                yield
                yield dut.wbbus.dat_r       .eq(data)
                yield dut.wbbus.ack         .eq(1)
                yield
                yield dut.wbbus.stall       .eq(0)
                yield dut.wbbus.ack         .eq(0)

                data += 1

        with self.simulate(dut, traces=dut.ports()) as sim:
            sim.add_clock(1.0 / 100e6, domain='sync')
            sim.add_sync_process(bbus_process)
            sim.add_sync_process(wbbus_process)
