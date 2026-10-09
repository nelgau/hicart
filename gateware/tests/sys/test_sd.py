from amaranth import *
from amaranth.sim import *

from hicart.sys.sd import SectorBuffer
from hicart.utils.sim import MultiProcessTestCase


class TestSectorBuffer(MultiProcessTestCase):

    def test_basic(self):
        dut = SectorBuffer(num_sectors=8)

        async def testbench(ctx):
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

            assert ((result >> 8) & 0xff) == 0xaa

        with self.simulate(dut) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(testbench)
