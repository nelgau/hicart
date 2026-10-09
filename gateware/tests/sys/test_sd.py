from amaranth import *
from amaranth.sim import *

from hicart.sys.sd import SDDataBuffer
from hicart.utils.sim import MultiProcessTestCase


class TestSectorBuffer(MultiProcessTestCase):

    def test_basic(self):
        dut = SDDataBuffer(num_sectors=2)

        async def testbench(ctx):
            ctx.set(dut.stb_bus.addr, 0x2)
            ctx.set(dut.stb_bus.w_data, 0x55)
            ctx.set(dut.stb_bus.w_stb, 1)
            await ctx.tick()
            ctx.set(dut.stb_bus.w_stb, 0)
            await ctx.tick()

            ctx.set(dut.stb_bus.addr, 0x3)
            ctx.set(dut.stb_bus.w_data, 0xaa)
            ctx.set(dut.stb_bus.w_stb, 1)
            await ctx.tick()
            ctx.set(dut.stb_bus.w_stb, 0)
            await ctx.tick()

            ctx.set(dut.wb_bus.adr, 0x1)
            ctx.set(dut.wb_bus.cyc, 1)
            ctx.set(dut.wb_bus.stb, 1)

            while not ctx.get(dut.wb_bus.ack):
                await ctx.tick()

            result = ctx.get(dut.wb_bus.dat_r)
            await ctx.tick()

            assert result == 0xaa55

        with self.simulate(dut) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(testbench)

    def test_top(self):
        dut = SDDataBuffer(num_sectors=2)

        async def testbench(ctx):
            ctx.set(dut.stb_bus.addr, 0x3FF)
            ctx.set(dut.stb_bus.w_data, 0xaa)
            ctx.set(dut.stb_bus.w_stb, 1)
            await ctx.tick()
            ctx.set(dut.stb_bus.w_stb, 0)
            await ctx.tick()

            ctx.set(dut.wb_bus.adr, 0x1FF)
            ctx.set(dut.wb_bus.cyc, 1)
            ctx.set(dut.wb_bus.stb, 1)

            while not ctx.get(dut.wb_bus.ack):
                await ctx.tick()

            result = ctx.get(dut.wb_bus.dat_r)
            await ctx.tick()

            assert result == 0xaa00

    def test_wrap(self):
        dut = SDDataBuffer(num_sectors=2)

        async def testbench(ctx):
            ctx.set(dut.stb_bus.addr, 0x400)
            ctx.set(dut.stb_bus.w_data, 0xaa)
            ctx.set(dut.stb_bus.w_stb, 1)
            await ctx.tick()
            ctx.set(dut.stb_bus.w_stb, 0)
            await ctx.tick()

            ctx.set(dut.wb_bus.adr, 0x0)
            ctx.set(dut.wb_bus.cyc, 1)
            ctx.set(dut.wb_bus.stb, 1)

            while not ctx.get(dut.wb_bus.ack):
                await ctx.tick()

            result = ctx.get(dut.wb_bus.dat_r)
            await ctx.tick()

            assert result == 0x00aa

        with self.simulate(dut) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(testbench)
