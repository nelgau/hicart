import os
import pytest

from amaranth.sim import *

from hicart.n64.cic import CIC
from hicart.sim.behavioral.cic import CICCommand, CICDriver
from hicart.sim.testcase import MultiProcessTestCase


@pytest.mark.skipif(
    not os.getenv('HICART_TEST_CIC', default=False),
    reason="the runtime is too long"
)
class CICTest(MultiProcessTestCase):

    def test_reset(self):
        dut = CIC()
        driver = CICDriver(dut.bus, dut.reset)

        async def testbench(ctx):
            await driver.begin(ctx)

            hello1, seed1, checksum1 = await driver.receive_preamble(ctx)

            assert hello1 == 0x1
            assert seed1 == [0xB, 0xD, 0x3, 0x9, 0x3, 0xD]

            assert checksum1 == [
                0x9, 0x0, 0x4, 0x0, 0xA, 0xE, 0xC, 0xB,
                    0xF, 0xD, 0xA, 0xD, 0xB, 0x2, 0x6, 0x5]

            await driver.reset_device(ctx)

            hello2, seed2, checksum2 = await driver.receive_preamble(ctx)

            assert hello2 == 0x1
            assert seed2 == [0xB, 0xD, 0x3, 0x9, 0x3, 0xD]

            assert checksum2 == [
                0x9, 0x0, 0x4, 0x0, 0xA, 0xE, 0xC, 0xB,
                    0xF, 0xD, 0xA, 0xD, 0xB, 0x2, 0x6, 0x5]

        traces = [
            dut.reset,
            dut.bus.dclk.i,
            dut.bus.data.i,
            dut.bus.data.o,
            dut.bus.data.oe,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 100e6, domain="sync")
            sim.add_testbench(testbench)

    def test_output(self):
        dut = CIC()
        driver = CICDriver(dut.bus, dut.reset)

        async def testbench(ctx):
            hello, seed, checksum = await driver.receive_preamble(ctx)

            assert hello == 0x1
            assert seed == [0xB, 0xD, 0x3, 0x9, 0x3, 0xD]

            assert checksum == [
                    0x9, 0x0, 0x4, 0x0, 0xA, 0xE, 0xC, 0xB,
                        0xF, 0xD, 0xA, 0xD, 0xB, 0x2, 0x6, 0x5]

            await driver.send_initial_values(ctx, 0xA, 0x7)

            # Command 1
            await driver.send_command(ctx, CICCommand.COMPARE)
            cmd1_in_bits = await driver.exchange_for_compare(ctx, [
                    0, 1, 1, 0, 1, 1, 0])
            assert cmd1_in_bits == [
                    1, 1, 1, 0, 1, 0, 1]

            # Command 2
            await driver.send_command(ctx, CICCommand.COMPARE)
            cmd2_in_bits = await driver.exchange_for_compare(ctx, [
                    1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1])
            assert cmd2_in_bits == [
                    0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0]

        traces = [
            dut.reset,
            dut.bus.dclk.i,
            dut.bus.data.i,
            dut.bus.data.o,
            dut.bus.data.oe,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 100e6, domain="sync")
            sim.add_testbench(testbench)
