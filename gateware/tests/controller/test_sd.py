from amaranth import *
from amaranth.sim import *

from hicart.controller import sd
from hicart.utils.sim import MultiProcessTestCase


class TestSDClocker(MultiProcessTestCase):

    def test_basic(self):
        dut = sd.Clocker()

        async def testbench(ctx):
            assert ctx.get(dut.sd_clk) == 0
            assert ctx.get(dut.sd_clk_rising) == 0
            assert ctx.get(dut.sd_clk_falling) == 0

            await ctx.tick()

            assert ctx.get(dut.sd_clk) == 0
            assert ctx.get(dut.sd_clk_rising) == 0
            assert ctx.get(dut.sd_clk_falling) == 0

            ctx.set(dut.enable, 1)
            ctx.set(dut.divisor, 5)

            assert ctx.get(dut.sd_clk) == 0
            assert ctx.get(dut.sd_clk_rising) == 1
            assert ctx.get(dut.sd_clk_falling) == 0

            await ctx.tick()

            assert ctx.get(dut.sd_clk) == 1
            assert ctx.get(dut.sd_clk_rising) == 0
            assert ctx.get(dut.sd_clk_falling) == 0

            await ctx.tick().repeat(4)

            assert ctx.get(dut.sd_clk) == 1
            assert ctx.get(dut.sd_clk_rising) == 0
            assert ctx.get(dut.sd_clk_falling) == 1

            await ctx.tick()

            assert ctx.get(dut.sd_clk) == 0
            assert ctx.get(dut.sd_clk_rising) == 0
            assert ctx.get(dut.sd_clk_falling) == 0

            await ctx.tick().repeat(4)

            assert ctx.get(dut.sd_clk) == 0
            assert ctx.get(dut.sd_clk_rising) == 1
            assert ctx.get(dut.sd_clk_falling) == 0

            await ctx.tick()

            assert ctx.get(dut.sd_clk) == 1
            assert ctx.get(dut.sd_clk_rising) == 0
            assert ctx.get(dut.sd_clk_falling) == 0

        with self.simulate(dut) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(testbench)


class TestCmdTx(MultiProcessTestCase):

    def test_cmd8(self):
        clocker = sd.Clocker()
        dut = sd.CmdTx()

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += [
            dut.sd_clk_rising.eq(clocker.sd_clk_rising),
            dut.sd_clk_falling.eq(clocker.sd_clk_falling),
        ]

        async def testbench(ctx):
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.divisor, 2)

            ctx.set(dut.cmd_index, 8)
            ctx.set(dut.cmd_arg, 0x000001AA)
            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            # Wait for start bit
            await ctx.tick().until(dut.sd_cmd_oe & ~dut.sd_cmd_o)

            bytes = []
            for _ in range(6):
                byte = 0
                for _ in range(8):
                    await ctx.posedge(clocker.sd_clk)
                    bit = ctx.get(Mux(dut.sd_cmd_oe, dut.sd_cmd_o, 1))
                    byte = (byte << 1) | bit
                bytes.append(byte)

            assert bytes == [0x48, 0x00, 0x00, 0x01, 0xaa, 0x87]

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(testbench)


class TestSDController(MultiProcessTestCase):

    def test_basic(self):
        dut = sd.SDController()

        async def testbench(ctx):
            await ctx.tick().repeat(1000)

        traces = [
            dut.bus,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(testbench)
