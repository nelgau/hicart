from dataclasses import dataclass

from amaranth.sim import *

@dataclass
class _Task:
    address: int
    is_write: bool
    write_data: int


class WishboneEmulator:

    def __init__(self, bus, *, initial=0, delay=0, max_outstanding=None):
        self.bus = bus

        self.delay = delay
        self.max_outstanding = max_outstanding

        self.counter = initial
        self.stalled = False

        self._reset_pipeline()

    def emulate(self):
        while True:
            if not (yield self.bus.cyc):
                self._reset_pipeline()

            yield from self._accept_task()
            yield from self._finalize_next_task()
            yield from self._stall_if_needed()            
            yield

    def num_accepted_tasks(self):
        return sum(t is not None for t in self.pipeline)

    def _reset_pipeline(self):
        self.pipeline = [None for _ in range(self.delay)]

    def _accept_task(self):
        did_accept = (yield self.bus.cyc & self.bus.stb) and not self.stalled

        if did_accept:
            self.pipeline.append(_Task(
                (yield self.bus.adr),
                (yield self.bus.we),
                (yield self.bus.dat_w)
            ))
        else:
            self.pipeline.append(None)

    def _finalize_next_task(self):
        task, self.pipeline = self.pipeline[0], self.pipeline[1:]

        ack = False
        data = 0        

        if task is not None:
            ack = True
            data = self._dispatch_task(task)

        yield self.bus.ack.eq(ack)
        yield self.bus.dat_r.eq(data)

    def _stall_if_needed(self):
        if self.max_outstanding:
            self.stalled = self.num_accepted_tasks() >= self.max_outstanding
            yield self.bus.stall.eq(self.stalled)

    def _dispatch_task(self, task):
        if task.is_write:
            return 0

        result = self.counter
        self.counter += 1
        return result
