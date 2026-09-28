from amaranth.sim import *

from hicart.n64.pi import PISeqBridge
from hicart.soc import seqbus
from hicart.utils.sim import MultiProcessTestCase


class PISeqBridgeTest(MultiProcessTestCase):

    def test_basic(self):
        dut = PISeqBridge()

        sub_responder = seqbus.SeqbusResponder(dut.seq, initial=0xFACE, delay=1)

        async def sub_process(ctx):
            await sub_responder.run(ctx)

        async def intr_testbench(ctx):
            # Ale_l is active in idle state
            ctx.set(dut.pi.ale_l, 1)
            ctx.set(dut.pi.ale_h, 0)
            await ctx.tick().repeat(6)

            # Latch address

            ctx.set(dut.pi.ale_l, 0)
            await ctx.tick().repeat(2)
            ctx.set(dut.pi.ad.i, 0x1000)
            await ctx.tick().repeat(2)
            ctx.set(dut.pi.ale_h, 1)
            await ctx.tick().repeat(2)
            ctx.set(dut.pi.ad.i, 0x0002)
            await ctx.tick().repeat(2)
            ctx.set(dut.pi.ale_l, 1)
            await ctx.tick().repeat(8)

            # Read

            for i in range(3):
                ctx.set(dut.pi.read, 1)
                await ctx.tick().repeat(6)

                assert ctx.get(dut.pi.ad.o) == 0xFACE + i
                assert ctx.get(dut.pi.ad.oe) == 1

                ctx.set(dut.pi.read, 0)
                await ctx.tick().repeat(6)

                assert ctx.get(dut.pi.ad.oe) == 0

            # Ale_l is active in idle state
            ctx.set(dut.pi.ale_l, 1)
            ctx.set(dut.pi.ale_h, 0)
            await ctx.tick().repeat(6)

        traces = [
            dut.pi,
            dut.seq,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 80e6, domain="sync")
            sim.add_process(sub_process)
            sim.add_testbench(intr_testbench)
