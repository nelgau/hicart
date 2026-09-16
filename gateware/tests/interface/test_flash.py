from amaranth.sim import *

from hicart.interface.flash import FlashInterface, FlashWishboneInterface
from hicart.sim.testcase import MultiProcessTestCase


class FlashInterfaceTest(MultiProcessTestCase):

    def test_basic(self):
        dut = FlashInterface()

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
                ctx.set(dut.qspi_ce.d.i, x)
                await ctx.tick()

            ctx.set(dut.qspi_ce.d.i, 0)
            await ctx.tick()

            await ctx.tick().repeat(5)

            #

            ctx.set(dut.address, 0x876544)
            ctx.set(dut.start, 1)
            await ctx.tick()
            ctx.set(dut.start, 0)

            for x in [0x7, 0x6, 0x5, 0x4, 0x3, 0x2, 0x1, 0x0]:
                ctx.set(dut.qspi_ce.d.i, x)
                await ctx.tick()

            ctx.set(dut.qspi_ce.d.i, 0)
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
                ctx.set(dut.qspi_ce.d.i, x)
                await ctx.tick()

            ctx.set(dut.qspi_ce.d.i, 0)
            await ctx.tick()

            await ctx.tick().repeat(20)

        traces = [
            dut.qspi_ce.cs_n,
            dut.qspi_ce.sck_en,
            dut.qspi_ce.d.i,
            dut.qspi_ce.d.o,
            dut.qspi_ce.d.oe,

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


class FlashWishboneInterfaceTest(MultiProcessTestCase):

    def test_basic(self):
        dut = FlashWishboneInterface()

        async def testbench(ctx):
            await ctx.tick().repeat(10)

            #

            ctx.set(dut.bus.adr, 0x876543)
            ctx.set(dut.bus.cyc, 1)
            ctx.set(dut.bus.stb, 1)
            await ctx.tick()
            ctx.set(dut.bus.stb, 0)
            await ctx.tick()

            await ctx.tick().repeat(20)

            for x in [0xF, 0xE, 0xD, 0xC, 0xB, 0xA, 0x9, 0x8]:
                ctx.set(dut.qspi_ce.d.i, x)
                await ctx.tick()

            ctx.set(dut.qspi_ce.d.i, 0)
            await ctx.tick()

            ctx.set(dut.bus.cyc, 0)
            await ctx.tick()

            await ctx.tick().repeat(5)


            #

            ctx.set(dut.bus.adr, 0x876544)
            ctx.set(dut.bus.cyc, 1)
            ctx.set(dut.bus.stb, 1)
            await ctx.tick()
            ctx.set(dut.bus.stb, 0)

            for x in [0x7, 0x6, 0x5, 0x4, 0x3, 0x2, 0x1, 0x0]:
                ctx.set(dut.qspi_ce.d.i, x)
                await ctx.tick()

            ctx.set(dut.qspi_ce.d.i, 0)
            await ctx.tick()

            ctx.set(dut.bus.cyc, 0)
            await ctx.tick()

            await ctx.tick().repeat(5)

            #

            ctx.set(dut.bus.adr, 0x876546)
            ctx.set(dut.bus.cyc, 1)
            ctx.set(dut.bus.stb, 1)
            await ctx.tick()
            ctx.set(dut.bus.stb, 0)
            await ctx.tick()

            await ctx.tick().repeat(28)

            for x in [0xC, 0xA, 0xF, 0xE, 0xB, 0xA, 0xB, 0xE]:
                ctx.set(dut.qspi_ce.d.i, x)
                await ctx.tick()

            ctx.set(dut.qspi_ce.d.i, 0)
            await ctx.tick()

            ctx.set(dut.bus.cyc, 0)
            await ctx.tick()

            await ctx.tick().repeat(20)

        traces = [
            dut.qspi_ce.cs_n,
            dut.qspi_ce.sck_en,
            dut.qspi_ce.d.i,
            dut.qspi_ce.d.o,
            dut.qspi_ce.d.oe,

            dut.bus.cyc,
            dut.bus.stb,
            dut.bus.stall,
            dut.bus.ack,
            dut.bus.adr,
            dut.bus.dat_r
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 100e6, domain="sync")
            sim.add_testbench(testbench)
