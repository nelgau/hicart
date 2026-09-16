import os
import re
import unittest
from contextlib import contextmanager

from amaranth import *
from amaranth.sim import *


class MultiProcessTestCase(unittest.TestCase):

    @contextmanager
    def simulate(self, dut, *, traces=()):
        sim = Simulator(dut)

        yield sim

        if os.getenv('GENERATE_VCDS', default=False):
            # Create an output directory
            os.makedirs("traces", exist_ok=True)
            # Figure out the name of our VCD files
            trace_name = "traces/" + self.id()

            all_traces = []
            # Add clock signals to the traces by default
            fragment = sim._design.fragment
            for domain in fragment.iter_domains():
                cd = fragment.domains[domain]
                all_traces.extend((cd.clk, cd.rst))

            # Add any user-supplied traces after the clock domains
            all_traces += _flatten_traces(traces)

            for t in all_traces:
                print(t.name)

            vcd_name = trace_name + ".vcd"
            gtkw_name = trace_name + ".gtkw"
            surfer_name = trace_name + ".sucl"

            # ... and run the simulation while writing them.
            with _write_surfer_commands(gtkw_name, surfer_name):
                with sim.write_vcd(vcd_name, gtkw_name, traces=all_traces):
                    sim.run()
        else:
            sim.run()


def _flatten_traces(traces):
    all_signals = []

    def iter_record(record):
        for field_name, field in record.fields.items():
            if isinstance(field, Record):
                yield from iter_record(field)
            else:
                yield field

    def iter_interface(interface):
        for name in interface.signature.members:
            obj = getattr(interface, name)
            if isinstance(obj, Signal):
                yield obj
            elif hasattr(obj, "signature"):
                yield from iter_interface(obj)

    # Add any user-supplied traces after the clock domains
    for trace in traces:
        if isinstance(trace, Signal):
            all_signals.append(trace)
        elif isinstance(trace, Record):
            for t in iter_record(trace):
                all_signals.append(t)
        elif hasattr(trace, "signature"):
            for t in iter_interface(trace):
                all_signals.append(t)
        else:
            raise TypeError("Trace is not a singal, record, or interface.")

    return all_signals

@contextmanager
def _write_surfer_commands(gtkw_name, surfer_name):
    yield

    kv_pattern = re.compile(r"\[(?P<key>.*?)\]\s*\"?(?P<value>.*?)\"?$")
    type_pattern = re.compile(r"@(?P<type_id>.*)$")
    signal_pattern = re.compile(r"(?P<name>.*?)(\[(?P<range>.*?)\])?$")

    with open(surfer_name, "w") as surfer_file:
        with open(gtkw_name, "r") as gtkw_file:
            for line in gtkw_file:
                line = line.strip()

                if not line:
                    continue

                match line[0]:
                    case "[":
                        match = kv_pattern.match(line)
                        key, value = match.group("key", "value")

                        if key == "dumpfile":
                            surfer_file.write(f"load_file {value}\n")
                    case "@":
                        match = type_pattern.match(line)
                        _ = match.group("type_id")
                    case _:
                        match = signal_pattern.match(line)
                        name, _ = match.group("name", "range")

                        surfer_file.write(f"variable_add {name}\n")
