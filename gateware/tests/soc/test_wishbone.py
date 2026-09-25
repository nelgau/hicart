from amaranth.sim import *
from amaranth_soc import wishbone
from amaranth_soc.memory import MemoryMap

from hicart.soc.wishbone import WindowMapper
from hicart.sim.testcase import MultiProcessTestCase


class WindowMapperTest(MultiProcessTestCase):

    def test_narrow(self):
        sub_bus = wishbone.Interface(addr_width=24, data_width=8)
        sub_bus.memory_map = MemoryMap(addr_width=24, data_width=8)

        dut = WindowMapper(sub_bus, addr_width=23, base_addr=0x800000)

        async def testbench(ctx):
            ctx.set(dut.bus.adr, 0x4000)
            assert ctx.get(sub_bus.adr) == 0x804000

        with self.simulate(dut) as sim:
            sim.add_testbench(testbench)

    def test_wide(self):
        sub_bus = wishbone.Interface(addr_width=23, data_width=16, granularity=8)
        sub_bus.memory_map = MemoryMap(addr_width=24, data_width=8)

        dut = WindowMapper(sub_bus, addr_width=22, base_addr=0x800000)

        async def testbench(ctx):
            ctx.set(dut.bus.adr, 0x2000)
            assert ctx.get(sub_bus.adr) == 0x402000

        with self.simulate(dut) as sim:
            sim.add_testbench(testbench)
