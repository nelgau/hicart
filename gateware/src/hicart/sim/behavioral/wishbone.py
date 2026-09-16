from dataclasses import dataclass
import time

from amaranth.sim import *


class WishboneInitiatorDriver:

    def __init__(self, bus):
        self.bus = bus

    async def begin(self, ctx):
        pass

    async def read_once(self, ctx, address):
        ctx.set(self.bus.cyc, 1)
        ctx.set(self.bus.we, 0)

        ctx.set(self.bus.stb, 1)
        ctx.set(self.bus.adr, address)

        while ctx.get(self.bus.stall):
            await ctx.tick()

        await ctx.tick()

        ctx.set(self.bus.stb, 0)

        while not ctx.get(self.bus.ack):
            await ctx.tick()

        result = ctx.get(self.bus.dat_r)
        await ctx.tick()

        ctx.set(self.bus.cyc, 0)
        await ctx.tick()

        return result

    async def read_sequential(self, ctx, count, start_address, stride):
        address = start_address
        stb_count = 0
        ack_count = 0
        cycles = 0
        result = []

        ctx.set(self.bus.cyc, 1)
        ctx.set(self.bus.we, 0)

        while ack_count < count:
            if stb_count < count:
                ctx.set(self.bus.adr, address)
                ctx.set(self.bus.stb, 1)

                if not ctx.get(self.bus.stall):
                    address += stride
                    stb_count += 1
            else:
                ctx.set(self.bus.stb, 0)
                ctx.set(self.bus.adr, 0)

            if ctx.get(self.bus.ack):
                result.append(ctx.get(self.bus.dat_r))
                ack_count += 1

            await ctx.tick()

            cycles += 1
            if cycles > 250:
                result = None
                break

        ctx.set(self.bus.cyc, 0)
        await ctx.tick()

        return result


class WishboneTargetResponder:

    @dataclass
    class _Task:
        address: int
        is_write: bool
        write_data: int

    def __init__(self, bus, *, initial=0, delay=0, max_outstanding=None):
        if delay < 0:
            raise ValueError(f"Delay must be non-negative")
        if max_outstanding is not None and max_outstanding < 1:
            raise ValueError(f"Max outstanding must be None or positive")

        self.bus = bus

        self.delay = delay
        self.max_outstanding = max_outstanding

        self.counter = initial
        self.stalled = False

        self._reset_pipeline()

    async def run(self, ctx):
        ctx.set(self.bus.ack, 0)
        ctx.set(self.bus.dat_r, 0)
        ctx.set(self.bus.stall, 0)

        async for _, rst_active, cyc, stb, adr, we, dat_w in (
            ctx.tick().sample(
                self.bus.cyc,
                self.bus.stb,
                self.bus.adr,
                self.bus.we,
                self.bus.dat_w,
            )
        ):
            result = 0
            ack = False

            if rst_active or not cyc:
                self._reset_pipeline()
            else:
                new_task = None
                if cyc & stb and not self.stalled:
                    new_task = self._Task(adr, we, dat_w)

                self.pipeline.append(new_task)
                curr_task = self.pipeline.pop(0)

                if curr_task is not None:
                    result = self._dispatch_task(curr_task)
                    ack = True

            if self.max_outstanding is not None:
                self.stalled = self.num_accepted_tasks >= self.max_outstanding

            ctx.set(self.bus.ack, ack)
            ctx.set(self.bus.stall, self.stalled)
            ctx.set(self.bus.dat_r, result)

    @property
    def num_accepted_tasks(self):
        return sum(t is not None for t in self.pipeline)

    def _reset_pipeline(self):
        self.pipeline = [None for _ in range(self.delay)]

    def _dispatch_task(self, task):
        if task.is_write:
            return 0
        else:
            result = self.counter
            self.counter += 1
            return result
