from amaranth.sim import *

from hicart.controller.flash import FlashController, WishboneFlashController
from hicart.sim.testcase import MultiProcessTestCase


class FlashInterfaceTest(MultiProcessTestCase):

    def test_basic(self):
        dut = FlashController()

        async def testbench(ctx):
            await ctx.tick().repeat(10)

            #

            ctx.set(dut.address, 0x876543)
            ctx.set(dut.start, 1)
            await ctx.tick()
            ctx.set(dut.start, 0)
            await ctx.tick()

            await ctx.tick().repeat(20)

            for x in [0xF, 0xE, 0xD, 0xC, 0xB, 0xA, 0x9, 0x8]:
                ctx.set(dut.bus.d.i, x)
                await ctx.tick()

            ctx.set(dut.bus.d.i, 0)
            await ctx.tick()

            await ctx.tick().repeat(5)

            #

            ctx.set(dut.address, 0x876544)
            ctx.set(dut.start, 1)
            await ctx.tick()
            ctx.set(dut.start, 0)

            for x in [0x7, 0x6, 0x5, 0x4, 0x3, 0x2, 0x1, 0x0]:
                ctx.set(dut.bus.d.i, x)
                await ctx.tick()

            ctx.set(dut.bus.d.i, 0)
            await ctx.tick()

            await ctx.tick().repeat(5)

            #

            ctx.set(dut.address, 0x876546)
            ctx.set(dut.start, 1)
            await ctx.tick()
            ctx.set(dut.start, 0)
            await ctx.tick()

            await ctx.tick().repeat(28)

            for x in [0xC, 0xA, 0xF, 0xE, 0xB, 0xA, 0xB, 0xE]:
                ctx.set(dut.bus.d.i, x)
                await ctx.tick()

            ctx.set(dut.bus.d.i, 0)
            await ctx.tick()

            await ctx.tick().repeat(20)

        traces = [
            dut.bus.cs_n,
            dut.bus.sck_en,
            dut.bus.d.i,
            dut.bus.d.o,
            dut.bus.d.oe,

            dut.start,
            dut.address,
            dut.idle,
            dut.valid,
            dut.data,

            dut._in_shift,
            dut._out_shift,
            dut._counter,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 100e6, domain="sync")
            sim.add_testbench(testbench)


class WishboneFlashInterfaceTest(MultiProcessTestCase):

    def test_basic(self):
        dut = WishboneFlashController()

        async def testbench(ctx):
            await ctx.tick().repeat(10)

            #

            ctx.set(dut.wb.adr, 0x876543)
            ctx.set(dut.wb.cyc, 1)
            ctx.set(dut.wb.stb, 1)
            await ctx.tick()
            ctx.set(dut.wb.stb, 0)
            await ctx.tick()

            await ctx.tick().repeat(20)

            for x in [0xF, 0xE, 0xD, 0xC, 0xB, 0xA, 0x9, 0x8]:
                ctx.set(dut.bus.d.i, x)
                await ctx.tick()

            ctx.set(dut.bus.d.i, 0)
            await ctx.tick()

            ctx.set(dut.wb.cyc, 0)
            await ctx.tick()

            await ctx.tick().repeat(5)


            #

            ctx.set(dut.wb.adr, 0x876544)
            ctx.set(dut.wb.cyc, 1)
            ctx.set(dut.wb.stb, 1)
            await ctx.tick()
            ctx.set(dut.wb.stb, 0)

            for x in [0x7, 0x6, 0x5, 0x4, 0x3, 0x2, 0x1, 0x0]:
                ctx.set(dut.bus.d.i, x)
                await ctx.tick()

            ctx.set(dut.bus.d.i, 0)
            await ctx.tick()

            ctx.set(dut.wb.cyc, 0)
            await ctx.tick()

            await ctx.tick().repeat(5)

            #

            ctx.set(dut.wb.adr, 0x876546)
            ctx.set(dut.wb.cyc, 1)
            ctx.set(dut.wb.stb, 1)
            await ctx.tick()
            ctx.set(dut.wb.stb, 0)
            await ctx.tick()

            await ctx.tick().repeat(28)

            for x in [0xC, 0xA, 0xF, 0xE, 0xB, 0xA, 0xB, 0xE]:
                ctx.set(dut.bus.d.i, x)
                await ctx.tick()

            ctx.set(dut.bus.d.i, 0)
            await ctx.tick()

            ctx.set(dut.wb.cyc, 0)
            await ctx.tick()

            await ctx.tick().repeat(20)

        traces = [
            dut.bus.cs_n,
            dut.bus.sck_en,
            dut.bus.d.i,
            dut.bus.d.o,
            dut.bus.d.oe,

            dut.wb.cyc,
            dut.wb.stb,
            dut.wb.stall,
            dut.wb.ack,
            dut.wb.adr,
            dut.wb.dat_r
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 100e6, domain="sync")
            sim.add_testbench(testbench)
