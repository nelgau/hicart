from amaranth.sim import *


class StreamDriver:

    def __init__(self, stream):
        self.stream = stream

    def begin(self):
        yield

    def produce(self, items):
        for item in items:
            yield self.stream.payload.eq(item)
            yield self.stream.valid.eq(1)
            yield Settle()

            # This is necessary because each stream transaction handshake must
            # span at least one simulation time step.
            did_advance = False

            while not (yield self.stream.ready):
                did_advance = True
                yield

            if not did_advance:
                yield

        yield self.stream.payload.eq(0)
        yield self.stream.valid.eq(0)
        yield

    def consume(self, count=1):
        results = []

        yield self.stream.ready.eq(1)
        yield Settle()

        while len(results) < count:
            # This is necessary because each stream transaction handshake must
            # span at least one simulation time step.
            did_advance = False

            while not (yield self.stream.valid):
                did_advance = True
                yield

            results.append((yield self.stream.payload))

            if not did_advance:
                yield

        yield self.stream.ready.eq(0)
        yield

        return results
