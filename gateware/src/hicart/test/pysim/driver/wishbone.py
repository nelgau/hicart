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
