import os
import math
import unittest
from functools import wraps

from amaranth.sim import Simulator

def sync_test_case(process_function):
    def run_test(self):
        @wraps(process_function)
        async def testbench(ctx):
            await self.initialize_signals(ctx)
            await process_function(self, ctx)

        self.sim.add_testbench(testbench)
        self.simulate()

    return run_test

class ModuleTestCase(unittest.TestCase):
    FRAGMENT_UNDER_TEST = None
    FRAGMENT_ARGUMENTS = {}

    CLOCK_FREQUENCY = 100e6

    def instantiate_dut(self):
        return self.FRAGMENT_UNDER_TEST(**self.FRAGMENT_ARGUMENTS)

    def setUp(self):
        self.dut = self.instantiate_dut()
        self.sim = Simulator(self.dut)
        self.sim.add_clock(1.0 / self.CLOCK_FREQUENCY, domain='sync')

    async def initialize_signals(self, ctx):
        pass

    def traces_of_interest(self):
        return ()

    def simulate(self, *, vcd_suffix=None):
        if os.getenv('GENERATE_VCDS', default=False):
            os.makedirs("traces", exist_ok=True)
            vcd_name = "traces/" + self.id()

            all_traces = []

            fragment = self.sim._design.fragment
            for domain in fragment.iter_domains():
                cd = fragment.domains[domain]
                all_traces.extend((cd.clk, cd.rst))

            all_traces += self.traces_of_interest()

            with self.sim.write_vcd(vcd_name + ".vcd", vcd_name + ".gtkw", traces=all_traces):
                self.sim.run()
        else:
            self.sim.run()

    @staticmethod
    def pulse(signal, *, step_after=True):
        """ Helper method that asserts a signal for a cycle. """
        yield signal.eq(1)
        yield
        yield signal.eq(0)

        if step_after:
            yield

    @staticmethod
    def advance_cycles(cycles):
        """ Helper method that waits for a given number of cycles. """
        for _ in range(cycles):
            yield

    @staticmethod
    def wait_until(strobe, *, timeout=None):
        """ Helper method that advances time until a strobe signal becomes true. """
        cycles_passed = 0

        while not (yield strobe):
            yield

            cycles_passed += 1
            if timeout and cycles_passed > timeout:
                raise RuntimeError(f"Timeout waiting for '{strobe.name}' to go high!")

    def wait(self, time):
        """ Helper method that waits for a given number of seconds. """
        period = 1 / self.CLOCK_FREQUENCY
        cycles = math.ceil(time / period)
        yield from self.advance_cycles(cycles)
