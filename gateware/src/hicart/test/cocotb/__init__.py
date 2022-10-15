import os
import unittest

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

from hicart.test.cocotb.accessor import Accessor
from hicart.test.cocotb.runner import run_test
from hicart.test import flatten_traces


def init_domains(dut):
    dut.clk.setimmediatevalue(0)
    dut.rst.setimmediatevalue(1)

def start_clock(handle, rate=100e6):
    period = int(1e9 / rate)
    clock = Clock(handle, period, units="ps")
    cocotb.start_soon(clock.start())

async def do_reset(dut):
    await RisingEdge(dut.clk)
    dut.rst.setimmediatevalue(1)
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)


class CocotbTestCase(unittest.TestCase):

    def simulate(self, dut, *, platform=None, traces=()):
        test_module, test_class, test_method = self.id().rsplit('.', 2)
        testcase = f"run_{test_class}_{test_method}"
        vcd_file = None

        if os.getenv('GENERATE_VCDS', default=False):
            # Create an output directory
            os.makedirs("traces", exist_ok=True)
            # Figure out the name of our VCD files
            vcd_file = os.path.join("traces", f"{self.id()}.vcd")

        # FIXME: Add clock and reset signals?
        all_traces = []

        # Add any user-supplied traces after the clock domains
        all_traces += flatten_traces(traces)

        run_test(
            design=dut,
            platform=platform,
            ports=all_traces,
            module=test_module,
            testcase=testcase,
            vcd_file=vcd_file,
        )
