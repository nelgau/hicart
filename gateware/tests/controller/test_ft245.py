from amaranth import *
from amaranth.sim import *

from hicart.controller.ft245 import FT245Controller
from hicart.utils.sim import MultiProcessTestCase
4

class FT245InterfaceTest(MultiProcessTestCase):

    def test_read(self):
        dut = FT245Controller()

        dut.bus.rxf = Signal(init=1)
        dut.bus.txe = Signal(init=1)

        async def testbench(ctx):
            await ctx.tick().repeat(2)

            ctx.set(dut.bus.rxf, 0)
            await ctx.tick().repeat(2)

            await ctx.tick().until(~dut.bus.rd)
            await ctx.tick().repeat(2)

            ctx.set(dut.bus.rxf, 1)
            ctx.set(dut.bus.d.i, 0xA9)

            await ctx.tick().until(dut.bus.rd)
            await ctx.tick().repeat(2)

            ctx.set(dut.bus.rxf, 1)
            ctx.set(dut.bus.d.i, 0)

            assert ctx.get(dut.rx.payload) == 0xA9
            assert ctx.get(dut.rx.valid) == 1

            ctx.set(dut.rx.ready, 1)
            await ctx.tick()

            ctx.set(dut.rx.ready, 0)
            await ctx.tick()

            assert ctx.get(dut.rx.valid) == 0

        traces = [
            dut.bus.d.i,
            dut.bus.d.o,
            dut.bus.d.oe,
            dut.bus.rxf,
            dut.bus.txe,
            dut.bus.rd,
            dut.bus.wr,

            dut.rx.payload,
            dut.rx.valid,
            dut.rx.ready,

            dut.tx.payload,
            dut.tx.valid,
            dut.tx.ready,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 100e6, domain="sync")
            sim.add_testbench(testbench)

    def test_write(self):
        dut = FT245Controller()

        dut.bus.rxf.i = Signal(init=1)
        dut.bus.txe.i = Signal(init=1)

        async def testbench(ctx):
            await ctx.tick().repeat(2)

            assert ctx.get(dut.tx.ready) == 1

            ctx.set(dut.tx.payload, 0xBB)
            ctx.set(dut.tx.valid, 1)
            await ctx.tick()

            ctx.set(dut.tx.valid, 0)
            ctx.set(dut.bus.txe, 0)

            await ctx.tick().until(~dut.bus.wr)

            assert ctx.get(dut.bus.d.o) == 0xBB
            assert ctx.get(dut.bus.d.oe) == 1

            await ctx.tick().until(dut.bus.wr)

            assert ctx.get(dut.bus.d.oe) == 0

        traces = [
            dut.bus.d.i,
            dut.bus.d.o,
            dut.bus.d.oe,
            dut.bus.rxf,
            dut.bus.txe,
            dut.bus.rd,
            dut.bus.wr,

            dut.rx.payload,
            dut.rx.valid,
            dut.rx.ready,

            dut.tx.payload,
            dut.tx.valid,
            dut.tx.ready,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 100e6, domain="sync")
            sim.add_testbench(testbench)
