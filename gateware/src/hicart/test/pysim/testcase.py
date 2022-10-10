import os
import unittest
from contextlib import contextmanager

from amaranth.sim import Simulator

from hicart.test import flatten_traces


class MultiProcessTestCase(unittest.TestCase):

    @contextmanager
    def simulate(self, dut, *, traces=()):
        sim = Simulator(dut)

        yield sim

        if os.getenv('GENERATE_VCDS', default=False):
            # Create an output directory
            os.makedirs("traces", exist_ok=True)
            # Figure out the name of our VCD files
            vcd_name = "traces/" + self.id()
            
            all_traces = []
            # Add clock signals to the traces by default
            fragment = sim._fragment
            for domain in fragment.iter_domains():
                cd = fragment.domains[domain]
                all_traces.extend((cd.clk, cd.rst))

            # Add any user-supplied traces after the clock domains
            all_traces += flatten_traces(traces)

            # ... and run the simulation while writing them.
            with sim.write_vcd(vcd_name + ".vcd", vcd_name + ".gtkw", traces=all_traces):
                sim.run()
        else:
            sim.run()
