from amaranth.sim import *

from hicart.n64.pi import PISeqBridge, PIInitiatorDriver
from hicart.soc import seqbus
from hicart.utils.sim import MultiProcessTestCase


class PISeqBridgeTest(MultiProcessTestCase):

    def test_read(self):
        dut = PISeqBridge()

        sub_responder = seqbus.SeqbusResponder(dut.seq, initial=0xFACE, delay=1)
        intr_driver = PIInitiatorDriver(dut.pi)

        async def sub_process(ctx):
            await sub_responder.run(ctx)

        async def intr_testbench(ctx):
            await intr_driver.begin(ctx)

            count = 2
            result = await intr_driver.read_burst_slow(ctx, 0x10000000, count)

            for i in range(count):
                assert result[i][0] == 0x10000000 + 2 * i
                assert result[i][1] == 0xFACE + i

        traces = [
            dut.pi,
            dut.seq,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 80e6, domain="sync")
            sim.add_process(sub_process)
            sim.add_testbench(intr_testbench)

    def test_write(self):
        dut = PISeqBridge()

        sub_responder = seqbus.SeqbusResponder(dut.seq, initial=0xFACE, delay=1)
        intr_driver = PIInitiatorDriver(dut.pi)

        async def sub_process(ctx):
            await sub_responder.run(ctx)

        async def intr_testbench(ctx):
            await intr_driver.begin(ctx)

            await intr_driver.write_burst(ctx, 0x10000000, [0xCAFE])
            result = await intr_driver.read_burst_slow(ctx, 0x10000000, 1)

            assert result[0][0] == 0x10000000
            assert result[0][1] == 0xCAFE

        traces = [
            dut.pi,
            dut.seq,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 80e6, domain="sync")
            sim.add_process(sub_process)
            sim.add_testbench(intr_testbench)
