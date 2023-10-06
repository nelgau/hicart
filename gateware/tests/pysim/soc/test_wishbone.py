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
        sub_bus = wishbone.Interface(addr_width=24, data_width=8, features={"stall"}, memory_map=sub_memory_map)

        dut = DownConverter(sub_bus=sub_bus, addr_width=22, data_width=32,
            granularity=8, features={"stall"})

        intr_driver = WishboneInitiatorDriver(dut.bus)
        sub_emulator = WishboneTargetEmulator(sub_bus, delay=1, max_outstanding=1)

        def intr_process():
            yield from intr_driver.begin()
            yield from intr_driver.read_sequential(5, 0x00040000, 7)

        def sub_process():
            yield Passive()
            yield from sub_emulator.emulate()

        with self.simulate(dut, traces=dut.ports()) as sim:
            sim.add_clock(1.0 / 100e6, domain='sync')
            sim.add_sync_process(intr_process)
            sim.add_sync_process(sub_process)        
