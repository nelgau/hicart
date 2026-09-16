from amaranth.sim import *

from hicart.soc.stream import ByteDownConverter
from hicart.sim.testcase import MultiProcessTestCase


class ByteDownConverterTest(MultiProcessTestCase):

    def test_basic(self):
        dut = ByteDownConverter(byte_width=4)

        async def testbench(ctx):
            assert ctx.get(dut.source.ready) == 1
            ctx.set(dut.source.payload, 0xCAFEBABE)
            ctx.set(dut.source.valid, 1)
            await ctx.tick()

            ctx.set(dut.source.valid, 0)
            await ctx.tick()

            assert ctx.get(dut.source.ready) == 0
            ctx.set(dut.source.payload, 0xDEADBEEF)
            ctx.set(dut.source.valid, 1)
            await ctx.tick()

            assert ctx.get(dut.sink.payload) == 0xBE
            assert ctx.get(dut.sink.valid) == 1
            ctx.set(dut.sink.ready, 1)
            await ctx.tick()

            assert ctx.get(dut.sink.payload) == 0xBA
            assert ctx.get(dut.sink.valid) == 1
            await ctx.tick()

            assert ctx.get(dut.sink.payload) == 0xFE
            assert ctx.get(dut.sink.valid) == 1
            await ctx.tick()

            assert ctx.get(dut.source.ready) == 1
            assert ctx.get(dut.sink.payload) == 0xCA
            assert ctx.get(dut.sink.valid) == 1
            await ctx.tick()

            assert ctx.get(dut.source.ready) == 0
            assert ctx.get(dut.sink.payload) == 0xEF
            assert ctx.get(dut.sink.valid) == 1
            ctx.set(dut.source.valid, 0)
            await ctx.tick()

            assert ctx.get(dut.sink.payload) == 0xBE
            assert ctx.get(dut.sink.valid) == 1
            await ctx.tick()

            assert ctx.get(dut.sink.payload) == 0xAD
            assert ctx.get(dut.sink.valid) == 1
            await ctx.tick()

            assert ctx.get(dut.sink.payload) == 0xDE
            assert ctx.get(dut.sink.valid) == 1
            await ctx.tick()

            assert ctx.get(dut.source.ready) == 1
            assert ctx.get(dut.sink.valid) == 0

        traces = [
            dut.source.payload,
            dut.source.valid,
            dut.source.ready,

            dut.sink.payload,
            dut.sink.valid,
            dut.sink.ready,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 100e6, domain="sync")
            sim.add_testbench(testbench)
