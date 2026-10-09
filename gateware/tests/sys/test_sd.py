from amaranth import *
from amaranth.sim import *

from hicart.soc import csr_ext
from hicart.sys.sd import SDBuffer, SDBufferWriter
from hicart.utils.sim import MultiProcessTestCase


class TestSDBuffer(MultiProcessTestCase):

    def test_basic(self):
        dut = SDBuffer(num_sectors=2)

        async def testbench(ctx):
            ctx.set(dut.writer_bus.addr, 0x2)
            ctx.set(dut.writer_bus.w_data, 0x55)
            ctx.set(dut.writer_bus.w_stb, 1)
            await ctx.tick()
            ctx.set(dut.writer_bus.w_stb, 0)
            await ctx.tick()

            ctx.set(dut.writer_bus.addr, 0x3)
            ctx.set(dut.writer_bus.w_data, 0xaa)
            ctx.set(dut.writer_bus.w_stb, 1)
            await ctx.tick()
            ctx.set(dut.writer_bus.w_stb, 0)
            await ctx.tick()

            ctx.set(dut.wb_bus.adr, 0x1)
            ctx.set(dut.wb_bus.cyc, 1)
            ctx.set(dut.wb_bus.stb, 1)

            while not ctx.get(dut.wb_bus.ack):
                await ctx.tick()

            result = ctx.get(dut.wb_bus.dat_r)
            await ctx.tick()

            assert result == 0x55aa

        with self.simulate(dut) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(testbench)

    def test_top(self):
        dut = SDBuffer(num_sectors=2)

        async def testbench(ctx):
            ctx.set(dut.writer_bus.addr, 0x3FF)
            ctx.set(dut.writer_bus.w_data, 0xaa)
            ctx.set(dut.writer_bus.w_stb, 1)
            await ctx.tick()
            ctx.set(dut.writer_bus.w_stb, 0)
            await ctx.tick()

            ctx.set(dut.wb_bus.adr, 0x1FF)
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

    def test_wrap(self):
        dut = SDBuffer(num_sectors=2)

        async def testbench(ctx):
            ctx.set(dut.writer_bus.addr, 0x400)
            ctx.set(dut.writer_bus.w_data, 0xaa)
            ctx.set(dut.writer_bus.w_stb, 1)
            await ctx.tick()
            ctx.set(dut.writer_bus.w_stb, 0)
            await ctx.tick()

            ctx.set(dut.wb_bus.adr, 0x0)
            ctx.set(dut.wb_bus.cyc, 1)
            ctx.set(dut.wb_bus.stb, 1)

            while not ctx.get(dut.wb_bus.ack):
                await ctx.tick()

            result = ctx.get(dut.wb_bus.dat_r)
            await ctx.tick()

            assert result == 0xaa00

        with self.simulate(dut) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(testbench)


class TestSDBufferWriter(MultiProcessTestCase):

    def test_basic(self):
        writer_bus = SDBuffer.WriterBusSignature(addr_width=8, data_width=8).create()
        dut = SDBufferWriter(writer_bus=writer_bus)

        bridge = csr_ext.WishboneCSRBridge(dut.csr_bus, data_width=32)

        m = Module()
        m.submodules.dut = dut
        m.submodules.bridge = bridge

        async def testbench(ctx):
            assert ctx.get(dut.writer_bus.addr) == 0x0
            assert ctx.get(dut.writer_bus.w_stb) == 0

            ctx.set(dut.sink.payload, 0xaa)
            ctx.set(dut.sink.valid, 1)

            assert ctx.get(dut.writer_bus.addr) == 0x0
            assert ctx.get(dut.writer_bus.w_data) == 0xaa
            assert ctx.get(dut.writer_bus.w_stb) == 1

            await ctx.tick()

            ctx.set(dut.sink.valid, 0)

            assert ctx.get(dut.writer_bus.addr) == 0x1
            assert ctx.get(dut.writer_bus.w_stb) == 0

            await ctx.tick()

            ctx.set(bridge.wb_bus.adr, 0x0)
            ctx.set(bridge.wb_bus.cyc, 1)
            ctx.set(bridge.wb_bus.stb, 1)
            ctx.set(bridge.wb_bus.sel, 0b1111)
            ctx.set(bridge.wb_bus.we, 1)
            ctx.set(bridge.wb_bus.dat_w, 0x5)

            while not ctx.get(bridge.wb_bus.ack):
                await ctx.tick()

            ctx.set(bridge.wb_bus.cyc, 0)
            ctx.set(bridge.wb_bus.stb, 0)

            assert ctx.get(dut.writer_bus.addr) == 0x5

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(testbench)
