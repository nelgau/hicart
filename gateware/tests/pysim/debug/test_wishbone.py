from amaranth import *
from amaranth.sim import *

from hicart.debug.wishbone import StreamWishboneCommander
from hicart.test.testcase import MultiProcessTestCase
from hicart.test.driver.stream import StreamDriver
from hicart.test.emulator.wishbone import WishboneEmulator


class StreamWishboneCommanderTest(MultiProcessTestCase):

    def test_simple(self):
        dut = StreamWishboneCommander()

        bus_emulator = WishboneEmulator(dut.bus, initial=0xFEEDFACE, delay=1, max_outstanding=1)
        source_driver = StreamDriver(dut.source)
        sink_driver = StreamDriver(dut.sink)

        def bus_process():
            yield Passive()
            yield from bus_emulator.emulate()

        def source_process():
            yield from source_driver.begin()

            # Read command
            yield from source_driver.produce([0x10])
            yield from source_driver.produce([0xCA, 0xFE, 0xBA, 0xBE])

            for i in range(4):
                yield

            # Write command
            yield from source_driver.produce([0x11])
            yield from source_driver.produce([0xDE, 0xAD, 0xBE, 0xEF])
            yield from source_driver.produce([0x12, 0x34, 0x56, 0x78])

        def sink_process():
            yield from sink_driver.begin()

            # Read command
            yield from sink_driver.consume(4)
            yield from sink_driver.consume()

            # Write command
            yield from sink_driver.consume()

        with self.simulate(dut, traces=dut.ports()) as sim:
            sim.add_clock(1.0 / 100e6, domain='sync')
            sim.add_sync_process(bus_process)
            sim.add_sync_process(source_process)
            sim.add_sync_process(sink_process)
