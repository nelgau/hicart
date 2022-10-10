from typing import Sequence, Union

from amaranth import *


def flatten_traces(traces: Sequence[Union[Value, Record]]) -> list[Value]:
    all_signals = []

    def iter_flat(record):
        for field_name, field in record.fields.items():
            if isinstance(field, Record):
                yield from iter_flat(field)
            else:
                yield field

    # Add any user-supplied traces after the clock domains
    for trace in traces:
        if isinstance(trace, Record):
            for t in iter_flat(trace):
                all_signals.append(t)
        else:
            all_signals.append(trace)

    return all_signals
