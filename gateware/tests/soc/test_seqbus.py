from amaranth import *
from amaranth.sim import *
from amaranth_soc.memory import MemoryMap

from hicart.soc import seqbus
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
