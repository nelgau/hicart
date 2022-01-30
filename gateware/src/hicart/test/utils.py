import os
import math
import unittest
from functools import wraps

from amaranth import Signal
from amaranth.sim import Simulator

def sync_test_case(process_function):
    """ Decorator that converts a function into a simple synchronous-process test case. """

    # This pattern is lifted from LUNA

    def run_test(self):
        @wraps(process_function)
        def test_case():
            yield from self.initialize_signals()
            yield from process_function(self)

        self.domain = 'sync'
        self._ensure_clocks_present()
        self.sim.add_sync_process(test_case, domain='sync')
        self.simulate()

    return run_test

class ModuleTestCase(unittest.TestCase):
    # Convenience property: if set, instantiate_dut will automatically create
    # the relevant fragment with FRAGMENT_ARGUMENTS.
    FRAGMENT_UNDER_TEST = None
    FRAGMENT_ARGUMENTS = {}

    # Convenience properties: if not None, a clock with the relevant frequency
    # will automatically be added.
    CLOCK_FREQUENCY = 100e6

    def instantiate_dut(self):
        """ Basic-most function to instantiate a device-under-test.

        By default, instantiates FRAGMENT_UNDER_TEST.
        """
        return self.FRAGMENT_UNDER_TEST(**self.FRAGMENT_ARGUMENTS)

    def setUp(self):
        self.dut = self.instantiate_dut()
        self.sim = Simulator(self.dut)
        self.sim.add_clock(1.0 / self.CLOCK_FREQUENCY, domain='sync')

    def initialize_signals(self):
        """ Provide an opportunity for the test apparatus to initialize signals. """
        yield Signal()

    def traces_of_interest(self):
        """ Returns an iterable of traces in any generated output. """
        return ()

    def simulate(self, *, vcd_suffix=None):
        """ Runs our core simulation. """

        # If we're generating VCDs, run the test under a VCD writer.
        if os.getenv('GENERATE_VCDS', default=False):
            # Create an output directory
            os.makedirs("traces", exist_ok=True)
            # Figure out the name of our VCD files
            vcd_name = "traces/" + self.id()
            
            all_traces = []
            # Add clock signals to the traces by default
            fragment = self.sim._fragment
            for domain in fragment.iter_domains():
                cd = fragment.domains[domain]
                all_traces.extend((cd.clk, cd.rst))
                
            # Add any user-supplied traces after the clock domains
            all_traces += self.traces_of_interest()

            # ... and run the simulation while writing them.
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

    def _ensure_clocks_present(self):
        pass

    def wait(self, time):
        """ Helper method that waits for a given number of seconds. """
        period = 1 / self.CLOCK_FREQUENCY
        cycles = math.ceil(time / period)
        yield from self.advance_cycles(cycles) 

