from amaranth.sim import *

from hicart.debug.wishbone import StreamWishboneCommander
from hicart.sim.behavioral.stream import StreamDriver
from hicart.sim.behavioral.wishbone import WishboneTargetResponder
from hicart.sim.testcase import MultiProcessTestCase


class StreamWishboneCommanderTest(MultiProcessTestCase):

    def test_simple(self):
        dut = StreamWishboneCommander()

        target_responder = WishboneTargetResponder(dut.bus, initial=0xFEEDFACE, delay=1, max_outstanding=1)
        source_driver = StreamDriver(dut.source)
        sink_driver = StreamDriver(dut.sink)

        async def target_process(ctx):
            await target_responder.run(ctx)

        async def source_testbench(ctx):
            await source_driver.begin(ctx)

            # Read command
            await source_driver.produce(ctx, [0x10])
            await source_driver.produce(ctx, [0xCA, 0xFE, 0xBA, 0xBE])

            for i in range(4):
                await ctx.tick()

            # Write command
            await source_driver.produce(ctx, [0x11])
            await source_driver.produce(ctx, [0xDE, 0xAD, 0xBE, 0xEF])
            await source_driver.produce(ctx, [0x12, 0x34, 0x56, 0x78])

        async def sink_testbench(ctx):
            await sink_driver.begin(ctx)

            # Read command
            await sink_driver.consume(ctx, 4)
            await sink_driver.consume(ctx)

            # Write command
            await sink_driver.consume(ctx)

        with self.simulate(dut, traces=dut.ports()) as sim:
            sim.add_clock(1.0 / 100e6, domain="sync")
            sim.add_process(target_process)
            sim.add_testbench(source_testbench)
            sim.add_testbench(sink_testbench)
