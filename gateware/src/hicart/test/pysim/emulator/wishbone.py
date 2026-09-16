from dataclasses import dataclass

from amaranth.sim import *


@dataclass
class _Task:
    address: int
    is_write: bool
    write_data: int


class WishboneTargetEmulator:

    def __init__(self, bus, *, initial=0, delay=0, max_outstanding=None):
        self.bus = bus

        self.delay = delay
        self.max_outstanding = max_outstanding

        self.counter = initial
        self.stalled = False

        self._reset_pipeline()

    async def emulate(self, ctx):
        while True:
            if not ctx.get(self.bus.cyc):
                self._reset_pipeline()

            self._stall_if_needed(ctx)
            self._accept_task(ctx)
            self._finalize_task(ctx)

            await ctx.tick()

    def num_accepted_tasks(self):
        return sum(t is not None for t in self.pipeline)

    def _reset_pipeline(self):
        self.pipeline = [None for _ in range(self.delay)]

    def _accept_task(self, ctx):
        did_accept = ctx.get(self.bus.cyc & self.bus.stb) and not self.stalled

        if did_accept:
            self.pipeline.append(_Task(
                ctx.get(self.bus.adr),
                ctx.get(self.bus.we),
                ctx.get(self.bus.dat_w)
            ))
        else:
            self.pipeline.append(None)

    def _finalize_task(self, ctx):
        task, self.pipeline = self.pipeline[0], self.pipeline[1:]

        ack = False
        data = 0

        if task is not None:
            ack = True
            data = self._dispatch_task(task)

        ctx.set(self.bus.ack, ack)
        ctx.set(self.bus.dat_r, data)

    def _stall_if_needed(self, ctx):
        if self.max_outstanding:
            self.stalled = self.num_accepted_tasks() >= self.max_outstanding
            ctx.set(self.bus.stall, self.stalled)

    def _dispatch_task(self, task):
        if task.is_write:
            return 0

        result = self.counter
        self.counter += 1
        return result
