from amaranth import *
from amaranth.sim import *
from amaranth.utils import log2_int
from amaranth_soc import wishbone
from amaranth_soc.memory import MemoryMap

from hicart.soc.wishbone import DownConverter
from hicart.test.pysim.testcase import MultiProcessTestCase
from hicart.test.pysim.driver.wishbone import WishboneInitiatorDriver
from hicart.test.pysim.emulator.wishbone import WishboneTargetEmulator


class DownConverterTest(MultiProcessTestCase):

    def test_simple(self):
        sub_memory_map = MemoryMap(addr_width=24, data_width=8)
        sub_bus = wishbone.Interface(addr_width=24, data_width=8, features={"stall"})
        sub_bus.memory_map = sub_memory_map

        dut = DownConverter(sub_bus=sub_bus, addr_width=22, data_width=32,
            granularity=8, features={"stall"})

        intr_driver = WishboneInitiatorDriver(dut.bus)
        sub_emulator = WishboneTargetEmulator(sub_bus, delay=1, max_outstanding=1)

        async def intr_process(ctx):
            await intr_driver.begin(ctx)
            await intr_driver.read_sequential(ctx, 5, 0x00040000, 7)

        async def sub_process(ctx):
            await sub_emulator.emulate(ctx)

        with self.simulate(dut, traces=dut.ports()) as sim:
            sim.add_clock(1.0 / 100e6, domain='sync')
            sim.add_testbench(sub_process, background=True)
            sim.add_testbench(intr_process)
