from amaranth import *
from amaranth.sim import *

from hicart.interface.qspi_flash import QSPIFlashInterface, QSPIFlashWishboneInterface
from hicart.test.pysim.utils import ModuleTestCase, sync_test_case


class QSPIFlashInterfaceTest(ModuleTestCase):
    FRAGMENT_UNDER_TEST = QSPIFlashInterface

    def traces_of_interest(self):
        return [
            self.dut.qspi.sck,
            self.dut.qspi.cs_n,
            self.dut.qspi.d.i,
            self.dut.qspi.d.o,
            self.dut.qspi.d.oe,

            self.dut.start,
            self.dut.address,
            self.dut.idle,
            self.dut.valid,
            self.dut.data,

            self.dut._in_shift,
            self.dut._out_shift,
            self.dut._counter,
        ]

    @sync_test_case
    async def test_basic(self, ctx):
        await ctx.tick().repeat(10)

        #

        ctx.set(self.dut.address, 0x876543)
        ctx.set(self.dut.start, 1)
        await ctx.tick()
        ctx.set(self.dut.start, 0)
        await ctx.tick()

        await ctx.tick().repeat(20)

        for x in [0xF, 0xE, 0xD, 0xC, 0xB, 0xA, 0x9, 0x8]:
            ctx.set(self.dut.qspi.d.i, x)
            await ctx.tick()

        ctx.set(self.dut.qspi.d.i, 0)
        await ctx.tick()

        await ctx.tick().repeat(5)

        #

        ctx.set(self.dut.address, 0x876544)
        ctx.set(self.dut.start, 1)
        await ctx.tick()
        ctx.set(self.dut.start, 0)

        for x in [0x7, 0x6, 0x5, 0x4, 0x3, 0x2, 0x1, 0x0]:
            ctx.set(self.dut.qspi.d.i, x)
            await ctx.tick()

        ctx.set(self.dut.qspi.d.i, 0)
        await ctx.tick()

        await ctx.tick().repeat(5)

        #

        ctx.set(self.dut.address, 0x876546)
        ctx.set(self.dut.start, 1)
        await ctx.tick()
        ctx.set(self.dut.start, 0)
        await ctx.tick()

        await ctx.tick().repeat(28)

        for x in [0xC, 0xA, 0xF, 0xE, 0xB, 0xA, 0xB, 0xE]:
            ctx.set(self.dut.qspi.d.i, x)
            await ctx.tick()

        ctx.set(self.dut.qspi.d.i, 0)
        await ctx.tick()

        await ctx.tick().repeat(20)


class QSPIFlashWishboneInterfaceTest(ModuleTestCase):
    FRAGMENT_UNDER_TEST = QSPIFlashWishboneInterface

    def traces_of_interest(self):
        return [
            self.dut.qspi.sck,
            self.dut.qspi.cs_n,
            self.dut.qspi.d.i,
            self.dut.qspi.d.o,
            self.dut.qspi.d.oe,

            self.dut.bus.cyc,
            self.dut.bus.stb,
            self.dut.bus.stall,
            self.dut.bus.ack,
            self.dut.bus.adr,
            self.dut.bus.dat_r
        ]

    @sync_test_case
    async def test_basic(self, ctx):
        await ctx.tick().repeat(10)

        #

        ctx.set(self.dut.bus.adr, 0x876543)
        ctx.set(self.dut.bus.cyc, 1)
        ctx.set(self.dut.bus.stb, 1)
        await ctx.tick()
        ctx.set(self.dut.bus.stb, 0)
        await ctx.tick()

        await ctx.tick().repeat(20)

        for x in [0xF, 0xE, 0xD, 0xC, 0xB, 0xA, 0x9, 0x8]:
            ctx.set(self.dut.qspi.d.i, x)
            await ctx.tick()

        ctx.set(self.dut.qspi.d.i, 0)
        await ctx.tick()

        ctx.set(self.dut.bus.cyc, 0)
        await ctx.tick()

        await ctx.tick().repeat(5)


        #

        ctx.set(self.dut.bus.adr, 0x876544)
        ctx.set(self.dut.bus.cyc, 1)
        ctx.set(self.dut.bus.stb, 1)
        await ctx.tick()
        ctx.set(self.dut.bus.stb, 0)

        for x in [0x7, 0x6, 0x5, 0x4, 0x3, 0x2, 0x1, 0x0]:
            ctx.set(self.dut.qspi.d.i, x)
            await ctx.tick()

        ctx.set(self.dut.qspi.d.i, 0)
        await ctx.tick()

        ctx.set(self.dut.bus.cyc, 0)
        await ctx.tick()

        await ctx.tick().repeat(5)

        #

        ctx.set(self.dut.bus.adr, 0x876546)
        ctx.set(self.dut.bus.cyc, 1)
        ctx.set(self.dut.bus.stb, 1)
        await ctx.tick()
        ctx.set(self.dut.bus.stb, 0)
        await ctx.tick()

        await ctx.tick().repeat(28)

        for x in [0xC, 0xA, 0xF, 0xE, 0xB, 0xA, 0xB, 0xE]:
            ctx.set(self.dut.qspi.d.i, x)
            await ctx.tick()

        ctx.set(self.dut.qspi.d.i, 0)
        await ctx.tick()

        ctx.set(self.dut.bus.cyc, 0)
        await ctx.tick()

        await ctx.tick().repeat(20)
