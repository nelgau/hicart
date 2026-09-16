from amaranth import *
from amaranth.sim import *

from hicart.debug.wishbone import StreamWishboneCommander
from hicart.test.pysim.testcase import MultiProcessTestCase
from hicart.test.pysim.driver.stream import StreamDriver
from hicart.test.pysim.emulator.wishbone import WishboneTargetEmulator


class StreamWishboneCommanderTest(MultiProcessTestCase):

    def test_simple(self):
        dut = StreamWishboneCommander()

        bus_emulator = WishboneTargetEmulator(dut.bus, initial=0xFEEDFACE, delay=1, max_outstanding=1)
        source_driver = StreamDriver(dut.source)
        sink_driver = StreamDriver(dut.sink)

        async def bus_process(ctx):
            await bus_emulator.emulate(ctx)

        async def source_process(ctx):
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

        async def sink_process(ctx):
            await sink_driver.begin(ctx)

            # Read command
            await sink_driver.consume(ctx, 4)
            await sink_driver.consume(ctx)

            # Write command
            await sink_driver.consume(ctx)

        with self.simulate(dut, traces=dut.ports()) as sim:
            sim.add_clock(1.0 / 100e6, domain='sync')
            sim.add_testbench(bus_process, background=True)
            sim.add_testbench(source_process)
            sim.add_testbench(sink_process)
