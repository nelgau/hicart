from enum import IntEnum

from amaranth.sim import *


class CICCommand(IntEnum):
    COMPARE = 0
    DIE = 1
    CIC6105 = 2
    RESET = 3


class CICDriver:

    def __init__(self, bus, reset_signal):
        self.bus = bus
        self.reset_signal = reset_signal

    async def begin(self, ctx):
        ctx.set(self.reset_signal, 0)
        ctx.set(self.bus.dclk.i, 1)
        ctx.set(self.bus.data.i, 1)

    async def reset_device(self, ctx):
        ctx.set(self.reset_signal, 1)
        await ctx.delay(20e-6)
        ctx.set(self.reset_signal, 0)

    async def receive_preamble(self, ctx):
        await ctx.delay(20e-6)
        hello = await self._read_nibble(ctx)
        seed  = await self._read_nibbles(ctx, 6)

        await ctx.delay(70e-6)
        _ = await self._read_bit(ctx) # ignored
        checksum = await self._read_nibbles(ctx, 16)

        return (hello, seed, checksum)

    async def send_initial_values(self, ctx, n1, n2):
        await ctx.delay(20e-6)
        await self._write_nibble(ctx, n1)
        await self._write_nibble(ctx, n2)

    async def send_command(self, ctx, command):
        await ctx.delay(20e-6)
        await self._write_bit(ctx, command.value & 0x2)
        await self._write_bit(ctx, command.value & 0x1)

    async def exchange_for_compare(self, ctx, out_bits):
        await ctx.delay(200e-6)
        in_bits = []
        for out_bit in out_bits:
            await self._write_bit(ctx, out_bit)
            in_bit = await self._read_bit(ctx)
            in_bits.append(in_bit)
        return in_bits

    async def _read_bit(self, ctx):
        ctx.set(self.bus.dclk.i, 0)
        await ctx.delay(5e-6)

        # As the signal is pulled high externally, the bit is low if oe & ~o.
        bit = ctx.get(~self.bus.data.oe | self.bus.data.o)

        ctx.set(self.bus.dclk.i, 1)
        await ctx.delay(5e-6)

        return bit

    async def _read_nibble(self, ctx ):
        nibble = 0
        for _ in range(4):
            nibble <<= 1
            nibble |= await self._read_bit(ctx)

        await ctx.delay(10e-6)

        return nibble

    async def _read_nibbles(self, ctx, length):
        nibbles = []
        for _ in range(length):
            nibble = await self._read_nibble(ctx)
            nibbles.append(nibble)
        return nibbles

    async def _write_bit(self, ctx, bit):
        if bit == 0:
            ctx.set(self.bus.data.i, 0)

        ctx.set(self.bus.dclk.i, 0)
        await ctx.delay(5e-6)

        ctx.set(self.bus.dclk.i, 1)
        await ctx.delay(1e-6)

        ctx.set(self.bus.data.i, 1)
        await ctx.delay(4e-6)

    async def _write_nibble(self, ctx, nibble):
        await self._write_bit(ctx, nibble & 0x8)
        await self._write_bit(ctx, nibble & 0x4)
        await self._write_bit(ctx, nibble & 0x2)
        await self._write_bit(ctx, nibble & 0x1)
        await ctx.delay(10e-6)
