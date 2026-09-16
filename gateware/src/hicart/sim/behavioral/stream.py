from amaranth.sim import *


class StreamDriver:

    def __init__(self, stream):
        self.stream = stream

    async def begin(self, ctx):
        pass

    async def produce(self, ctx, items):
        ctx.set(self.stream.valid, 1)

        for item in items:
            ctx.set(self.stream.payload, item)

            while not ctx.get(self.stream.ready):
                await ctx.tick()

            await ctx.tick()

        ctx.set(self.stream.payload, 0)
        ctx.set(self.stream.valid, 0)

    async def consume(self, ctx, count=1):
        results = []

        ctx.set(self.stream.ready, 1)

        while len(results) < count:
            while not ctx.get(self.stream.valid):
                await ctx.tick()

            results.append(ctx.get(self.stream.payload))
            await ctx.tick()

        ctx.set(self.stream.ready, 0)

        return results
