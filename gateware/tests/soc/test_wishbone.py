from amaranth.sim import *
from amaranth_soc import wishbone
from amaranth_soc.memory import MemoryMap

from hicart.soc.wishbone import DownConverter
from hicart.sim.behavioral.wishbone import WishboneInitiatorDriver
from hicart.sim.behavioral.wishbone import WishboneTargetResponder
from hicart.sim.testcase import MultiProcessTestCase


class DownConverterTest(MultiProcessTestCase):

    def test_simple(self):
        sub_memory_map = MemoryMap(addr_width=24, data_width=8)
        sub_bus = wishbone.Interface(addr_width=24, data_width=8, features={"stall"})
        sub_bus.memory_map = sub_memory_map

        dut = DownConverter(sub_bus=sub_bus, addr_width=22, data_width=32,
            granularity=8, features={"stall"})

        sub_responder = WishboneTargetResponder(sub_bus, delay=1, max_outstanding=1)
        intr_driver = WishboneInitiatorDriver(dut.bus)

        async def sub_process(ctx):
            await sub_responder.run(ctx)

        async def intr_testbench(ctx):
            await intr_driver.begin(ctx)
            await intr_driver.read_sequential(ctx, 5, 0x00040000, 7)

        with self.simulate(dut, traces=dut.ports()) as sim:
            sim.add_clock(1.0 / 100e6, domain="sync")
            sim.add_process(sub_process)
            sim.add_testbench(intr_testbench)
