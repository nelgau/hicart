from typing import Sequence, Union

from amaranth import *


def flatten_traces(traces):
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
