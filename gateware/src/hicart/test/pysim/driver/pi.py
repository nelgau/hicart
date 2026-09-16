from amaranth.sim import *

# N.B. The control signals (e.g., ale_l, ale_h, read, write) need to be inverted!

class PIInitiatorDriver:

    def __init__(self, pi):
        self.pi = pi

    async def begin(self, ctx):
        ctx.set(self.pi.ale_l.i, 1)
        ctx.set(self.pi.ale_h.i, 0)
        await ctx.delay(1e-6)

    async def read_burst_slow(self, ctx, start_address, word_count):
        ctx.set(self.pi.ale_l.i, 0)
        await ctx.delay(56e-9)
        ctx.set(self.pi.ad.i, (start_address >> 16) & 0xFFFF)
        await ctx.delay(56e-9)
        ctx.set(self.pi.ale_h.i, 1)
        await ctx.delay(56e-9)
        ctx.set(self.pi.ad.i, start_address & 0xFFFF)
        await ctx.delay(56e-9)
        ctx.set(self.pi.ale_l.i, 1)
        await ctx.delay(1040e-9)

        address = start_address
        result = []

        for i in range(word_count):
            ctx.set(self.pi.read.i, 1)
            await ctx.delay(304e-9)

            word = ctx.get(self.pi.ad.o)
            ctx.set(self.pi.read.i, 0)
            await ctx.delay(64e-9)

            result.append((address, word))
            address += 2

        ctx.set(self.pi.ale_h.i, 0)
        await ctx.delay(2256e-9)

        return result

    async def read_burst_fast(self, ctx, start_address, word_count):

        # N.B., This does NOT model the behavior of splitting long bursts into subbursts of at most 256 words.

        ctx.set(self.pi.ale_l.i, 0)
        await ctx.delay(20e-9)
        ctx.set(self.pi.ad.i, (start_address >> 16) & 0xFFFF)
        await ctx.delay(92e-9)
        ctx.set(self.pi.ale_h.i, 1)
        await ctx.delay(20e-9)
        ctx.set(self.pi.ad.i, start_address & 0xFFFF)
        await ctx.delay(92e-9)
        ctx.set(self.pi.ale_l.i, 1)
        await ctx.delay(1044e-9)

        address = start_address
        result = []

        for i in range(word_count):
            ctx.set(self.pi.read.i, 1)
            await ctx.delay(304e-9)

            word = ctx.get(self.pi.ad.o)
            ctx.set(self.pi.read.i, 0)
            await ctx.delay(416e-9)

            result.append((address, word))
            address += 2

        ctx.set(self.pi.ale_h.i, 0)
        await ctx.delay(32e-9)

        return result
