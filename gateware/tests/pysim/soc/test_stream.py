from amaranth import *
from amaranth.sim import *

from hicart.soc.stream import ByteDownConverter
from hicart.test.pysim.utils import ModuleTestCase, sync_test_case


class ByteDownConverterTest(ModuleTestCase):
    FRAGMENT_UNDER_TEST = ByteDownConverter
    FRAGMENT_ARGUMENTS = dict(byte_width=4)

    def traces_of_interest(self):
        return [
            self.dut.source.payload,
            self.dut.source.valid,
            self.dut.source.ready,

            self.dut.sink.payload,
            self.dut.sink.valid,
            self.dut.sink.ready,
        ]

    @sync_test_case
    async def test_basic(self, ctx):
        assert ctx.get(self.dut.source.ready) == 1
        ctx.set(self.dut.source.payload, 0xCAFEBABE)
        ctx.set(self.dut.source.valid, 1)
        await ctx.tick()

        ctx.set(self.dut.source.valid, 0)
        await ctx.tick()

        assert ctx.get(self.dut.source.ready) == 0
        ctx.set(self.dut.source.payload, 0xDEADBEEF)
        ctx.set(self.dut.source.valid, 1)
        await ctx.tick()

        assert ctx.get(self.dut.sink.payload) == 0xBE
        assert ctx.get(self.dut.sink.valid) == 1
        ctx.set(self.dut.sink.ready, 1)
        await ctx.tick()

        assert ctx.get(self.dut.sink.payload) == 0xBA
        assert ctx.get(self.dut.sink.valid) == 1
        await ctx.tick()

        assert ctx.get(self.dut.sink.payload) == 0xFE
        assert ctx.get(self.dut.sink.valid) == 1
        await ctx.tick()

        assert ctx.get(self.dut.source.ready) == 1
        assert ctx.get(self.dut.sink.payload) == 0xCA
        assert ctx.get(self.dut.sink.valid) == 1
        await ctx.tick()

        assert ctx.get(self.dut.source.ready) == 0
        assert ctx.get(self.dut.sink.payload) == 0xEF
        assert ctx.get(self.dut.sink.valid) == 1
        ctx.set(self.dut.source.valid, 0)
        await ctx.tick()

        assert ctx.get(self.dut.sink.payload) == 0xBE
        assert ctx.get(self.dut.sink.valid) == 1
        await ctx.tick()

        assert ctx.get(self.dut.sink.payload) == 0xAD
        assert ctx.get(self.dut.sink.valid) == 1
        await ctx.tick()

        assert ctx.get(self.dut.sink.payload) == 0xDE
        assert ctx.get(self.dut.sink.valid) == 1
        await ctx.tick()

        assert ctx.get(self.dut.source.ready) == 1
        assert ctx.get(self.dut.sink.valid) == 0
