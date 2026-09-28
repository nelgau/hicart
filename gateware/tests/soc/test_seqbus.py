from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out, flipped
from amaranth.sim import *
from amaranth_soc import wishbone
from amaranth_soc.wishbone.sram import WishboneSRAM
from amaranth_soc.memory import MemoryMap

from hicart.soc import seqbus
from hicart.soc.wishbone import WishbonePipelinedResponder
from hicart.utils.sim import MultiProcessTestCase


class DecoderTest(MultiProcessTestCase):

    class DUT(Elaboratable):
        def __init__(self):
            self.decoder = seqbus.Decoder(addr_width=31, data_width=16, granularity=8)

        def elaborate(self, platform):
            m = Module()

            m.domains += ClockDomain("sync")
            m.submodules.decoder = self.decoder

            return m

    def test_basic(self):
        dut = self.DUT()

        sub_bus = seqbus.Interface(addr_width=30, data_width=16, granularity=8)
        sub_bus.memory_map = MemoryMap(addr_width=31, data_width=8)

        dut.decoder.add(sub_bus, addr=0x80000000)

        sub_responder = seqbus.SeqbusResponder(sub_bus, initial=0xFACE, delay=2)
        intr_driver = seqbus.SeqbusDriver(dut.decoder.bus)

        async def sub_process(ctx):
            await sub_responder.run(ctx)

        async def intr_testbench(ctx):
            await intr_driver.begin(ctx)

            await ctx.tick()

            # Read command
            assert await intr_driver.read_once(ctx, 0x40000000, initial_delay=2) == 0xFACE
            assert await intr_driver.read_once(ctx, 0x40000000, initial_delay=2) == 0xFACF

        traces = [
            dut.decoder.bus,
            sub_bus,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 100e6, domain="sync")
            sim.add_process(sub_process)
            sim.add_testbench(intr_testbench)

    def test_sequential(self):
        dut = self.DUT()

        sub_bus = seqbus.Interface(addr_width=30, data_width=16, granularity=8)
        sub_bus.memory_map = MemoryMap(addr_width=31, data_width=8)

        dut.decoder.add(sub_bus, addr=0x80000000)

        sub_responder = seqbus.SeqbusResponder(sub_bus, initial=0xFACE, delay=2)
        intr_driver = seqbus.SeqbusDriver(dut.decoder.bus)

        async def sub_process(ctx):
            await sub_responder.run(ctx)

        async def intr_testbench(ctx):
            await intr_driver.begin(ctx)

            await ctx.tick()

            # Read command
            await intr_driver.read_sequential(ctx, 0x40000000, 10, initial_delay=2, delay=1)

        traces = [
            dut.decoder.bus,
            sub_bus,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 100e6, domain="sync")
            sim.add_process(sub_process)
            sim.add_testbench(intr_testbench)


class WishboneBridgeTest(MultiProcessTestCase):

    class MemoryDUT(wiring.Component):
        seq: In(seqbus.Signature(addr_width=31, data_width=16, granularity=8))

        def elaborate(self, platform):
            m = Module()

            sram = WishboneSRAM(size=0x1000, data_width=16, granularity=8, writable=True)

            decoder = wishbone.Decoder(addr_width=31, data_width=16, granularity=8)
            decoder.add(sram.wb_bus, addr=0x10000000)

            bridge = seqbus.WishboneBridge(decoder.bus)

            wiring.connect(m, bridge.seq, flipped(self.seq))

            m.submodules.sram = sram
            m.submodules.decoder = decoder
            m.submodules.bridge = bridge

            return m


    def test_read(self):
        sub_bus = flipped(wishbone.Interface(addr_width=31, data_width=16, granularity=8, features={"stall"}))
        sub_bus.memory_map = MemoryMap(addr_width=32, data_width=8)

        dut = seqbus.WishboneBridge(sub_bus)

        sub_responder = WishbonePipelinedResponder(sub_bus, initial=0xFACE, delay=2)
        intr_driver = seqbus.SeqbusDriver(dut.seq)

        async def sub_process(ctx):
            await sub_responder.run(ctx)

        async def intr_testbench(ctx):
            await intr_driver.begin(ctx)
            await ctx.tick()

            result = await intr_driver.read_sequential(ctx, 0x40000000, 10, initial_delay=40, delay=5)
            assert result == [0xFACE + i for i in range(10)]

            await ctx.tick().repeat(10)
            sub_responder.counter = 0xFACE

            result = await intr_driver.read_sequential(ctx, 0x40000000, 10, initial_delay=40, delay=5)
            assert result == [0xFACE + i for i in range(10)]

        traces = [
            dut.seq,
            sub_bus,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 100e6, domain="sync")
            sim.add_process(sub_process)
            sim.add_testbench(intr_testbench)

    def test_write(self):
        sub_bus = flipped(wishbone.Interface(addr_width=31, data_width=16, granularity=8, features={"stall"}))
        sub_bus.memory_map = MemoryMap(addr_width=32, data_width=8)

        dut = seqbus.WishboneBridge(sub_bus)

        sub_responder = WishbonePipelinedResponder(sub_bus, initial=0xFACE, delay=2)
        intr_driver = seqbus.SeqbusDriver(dut.seq)

        async def sub_process(ctx):
            await sub_responder.run(ctx)

        async def intr_testbench(ctx):
            await intr_driver.begin(ctx)
            await ctx.tick()

            await intr_driver.write_once(ctx, 0x40000000, 0xFACE, initial_delay=2)

        traces = [
            dut.seq,
            dut.wb,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 100e6, domain="sync")
            sim.add_process(sub_process)
            sim.add_testbench(intr_testbench)

    def test_loopback(self):
        dut = self.MemoryDUT()
        driver = seqbus.SeqbusDriver(dut.seq)

        async def testbench(ctx):
            await driver.begin(ctx)
            await ctx.tick()

            await driver.write_once(ctx, 0x8000000, 0xFACE, initial_delay=2)
            await ctx.tick().repeat(2)

            result = await driver.read_once(ctx, 0x8000000, initial_delay=10)
            assert result == 0xFACE

        traces = [
            dut.seq,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 100e6, domain="sync")
            sim.add_testbench(testbench)


class PrefetchingWishboneBridgeTest(MultiProcessTestCase):

    def test_read(self):
        sub_bus = flipped(wishbone.Interface(addr_width=31, data_width=16, granularity=8, features={"stall"}))
        sub_bus.memory_map = MemoryMap(addr_width=32, data_width=8)

        dut = seqbus.PrefetchingWishboneBridge(sub_bus)

        sub_responder = WishbonePipelinedResponder(sub_bus, initial=0xFACE, delay=2)
        intr_driver = seqbus.SeqbusDriver(dut.seq)

        async def sub_process(ctx):
            await sub_responder.run(ctx)

        async def intr_testbench(ctx):
            await intr_driver.begin(ctx)

            await ctx.tick()

            result = await intr_driver.read_sequential(ctx, 0x40000000, 10, initial_delay=40, delay=5)
            assert result == [0xFACE + i for i in range(10)]

            await ctx.tick().repeat(10)
            sub_responder.counter = 0xFACE

            result = await intr_driver.read_sequential(ctx, 0x40000000, 10, initial_delay=40, delay=5)
            assert result == [0xFACE + i for i in range(10)]

        traces = [
            dut.seq,
            sub_bus,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 100e6, domain="sync")
            sim.add_process(sub_process)
            sim.add_testbench(intr_testbench)

    def test_write(self):
        sub_bus = flipped(wishbone.Interface(addr_width=31, data_width=16, granularity=8, features={"stall"}))
        sub_bus.memory_map = MemoryMap(addr_width=32, data_width=8)

        dut = seqbus.PrefetchingWishboneBridge(sub_bus)

        sub_responder = WishbonePipelinedResponder(sub_bus, initial=0xFACE, delay=2)
        intr_driver = seqbus.SeqbusDriver(dut.seq)

        async def sub_process(ctx):
            await sub_responder.run(ctx)

        async def intr_testbench(ctx):
            await intr_driver.begin(ctx)

            await ctx.tick()

            await intr_driver.write_once(ctx, 0x40000000, 0xFACE, initial_delay=2)

        traces = [
            dut.seq,
            dut.wb,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 100e6, domain="sync")
            sim.add_process(sub_process)
            sim.add_testbench(intr_testbench)