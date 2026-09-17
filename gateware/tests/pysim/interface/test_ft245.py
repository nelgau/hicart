from amaranth import *
from amaranth.sim import *

from hicart.interface.ft245 import  FT245Interface
from hicart.test.pysim.utils import ModuleTestCase, sync_test_case


class FT245InterfaceTest(ModuleTestCase):
    FRAGMENT_UNDER_TEST = FT245Interface

    def instantiate_dut(self):
        dut = FT245Interface()

        dut.bus.rxf.i = Signal(reset=1)
        dut.bus.txe.i = Signal(reset=1)

        return dut

    def traces_of_interest(self):
        return [
            self.dut.bus.d.i,
            self.dut.bus.d.o,
            self.dut.bus.d.oe,
            self.dut.bus.rxf.i,
            self.dut.bus.txe.i,
            self.dut.bus.rd.o,
            self.dut.bus.wr.o,

            self.dut.rx.payload,
            self.dut.rx.valid,
            self.dut.rx.ready,

            self.dut.tx.payload,
            self.dut.tx.valid,
            self.dut.tx.ready,
        ]

    @sync_test_case
    async def test_read(self, ctx):
        await ctx.tick().repeat(2)

        ctx.set(self.dut.bus.rxf.i, 0)
        await ctx.tick().repeat(2)

        await ctx.tick().until(~self.dut.bus.rd.o)
        await ctx.tick().repeat(2)

        ctx.set(self.dut.bus.rxf.i, 1)
        ctx.set(self.dut.bus.d.i, 0xA9)

        await ctx.tick().until(self.dut.bus.rd.o)
        await ctx.tick().repeat(2)

        ctx.set(self.dut.bus.rxf.i, 1)
        ctx.set(self.dut.bus.d.i, 0)

        assert ctx.get(self.dut.rx.payload) == 0xA9
        assert ctx.get(self.dut.rx.valid) == 1

        ctx.set(self.dut.rx.ready, 1)
        await ctx.tick()

        ctx.set(self.dut.rx.ready, 0)
        await ctx.tick()

        assert ctx.get(self.dut.rx.valid) == 0

    @sync_test_case
    async def test_write(self, ctx):
        await ctx.tick().repeat(2)

        assert ctx.get(self.dut.tx.ready) == 1

        ctx.set(self.dut.tx.payload, 0xBB)
        ctx.set(self.dut.tx.valid, 1)
        await ctx.tick()

        ctx.set(self.dut.tx.valid, 0)
        ctx.set(self.dut.bus.txe.i, 0)

        await ctx.tick().until(~self.dut.bus.wr.o)

        assert ctx.get(self.dut.bus.d.o) == 0xBB
        assert ctx.get(self.dut.bus.d.oe) == 1

        await ctx.tick().until(self.dut.bus.wr.o)

        assert ctx.get(self.dut.bus.d.oe) == 0
