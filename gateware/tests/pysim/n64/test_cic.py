import os
import pytest

from amaranth import *
from amaranth.sim import *

from hicart.n64.cic import CIC
from hicart.test.pysim.utils import ModuleTestCase, sync_test_case


@pytest.mark.skipif(
    not os.getenv('HICART_TEST_CIC', default=False),
    reason="the runtime is too long"
)
class CICTest(ModuleTestCase):
    FRAGMENT_UNDER_TEST = CIC

    def traces_of_interest(self):
        return [
            self.dut.reset,
            self.dut.bus.dclk.i,
            self.dut.bus.data.i,
            self.dut.bus.data.o,
            self.dut.bus.data.oe,
        ]

    async def initialize_signals(self, ctx):
        ctx.set(self.dut.reset, 0)
        ctx.set(self.dut.bus.dclk.i, 1)
        ctx.set(self.dut.bus.data.i, 1)

    @sync_test_case
    async def test_reset(self, ctx):
        await ctx.delay(20e-6)

        # Preamble (from CIC)
        hello1 = await self.read_nibble(ctx)
        seed1  = await self.read_nibbles(ctx, 2)

        ctx.set(self.dut.reset, 1)
        await ctx.tick().repeat(10)
        ctx.set(self.dut.reset, 0)

        await ctx.delay(20e-6)

        # Preamble (from CIC)
        hello2 = await self.read_nibble(ctx)
        seed2  = await self.read_nibbles(ctx, 2)

        assert hello2 == 0x1
        assert seed2 == [0xB, 0xD]

    @sync_test_case
    async def test_output(self, ctx):
        await ctx.delay(50e-6)

        # Preamble (from CIC)

        hello = await self.read_nibble(ctx)
        seed  = await self.read_nibbles(ctx, 6)

        assert hello == 0x1
        assert seed == [0xB, 0xD, 0x3, 0x9, 0x3, 0xD]

        await ctx.delay(70e-6)
        await self.read_bit(ctx)

        checksum = await self.read_nibbles(ctx, 16)

        assert checksum == [
            0x9, 0x0, 0x4, 0x0, 0xA, 0xE, 0xC, 0xB,
                0xF, 0xD, 0xA, 0xD, 0xB, 0x2, 0x6, 0x5]

        # Initial values (from PIF)

        await ctx.delay(20e-6)

        await self.write_nibble(ctx, 0xA)
        await self.write_nibble(ctx, 0x7)

        # Command 1 (from PIF)

        await ctx.delay(20e-6)
        await self.write_bit(ctx, 0)
        await self.write_bit(ctx, 0)
        await ctx.delay(200e-6)

        # Exchange 1 (Bidirectional)

        cmd1_in_bits = await self.exchange_bits(ctx, [0, 1, 1, 0, 1, 1, 0])
        assert cmd1_in_bits == [1, 1, 1, 0, 1, 0, 1]

        # Command 2 (from PIF)

        await ctx.delay(20e-6)
        await self.write_bit(ctx, 0)
        await self.write_bit(ctx, 0)
        await ctx.delay(200e-6)

        # Exchange 2 (Bidirectional)

        cmd2_in_bits = await self.exchange_bits(ctx, [
            1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1])
        assert cmd2_in_bits == [
            0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0]

    async def read_bit(self, ctx):
        ctx.set(self.dut.bus.dclk.i, 0)
        await ctx.delay(5e-6)

        # As the signal is pulled high externally, the bit is low if oe & ~o.
        bit = ctx.get(~self.dut.bus.data.oe | self.dut.bus.data.o)

        ctx.set(self.dut.bus.dclk.i, 1)
        await ctx.delay(5e-6)

        return bit

    async def read_nibble(self, ctx ):
        nibble = 0
        for _ in range(4):
            nibble <<= 1
            nibble |= await self.read_bit(ctx)

        await ctx.delay(10e-6)

        return nibble

    async def read_nibbles(self, ctx, length):
        nibbles = []
        for _ in range(length):
            nibble = await self.read_nibble(ctx)
            nibbles.append(nibble)
        return nibbles

    async def write_bit(self, ctx, bit):
        if bit == 0:
            ctx.set(self.dut.bus.data.i, 0)

        ctx.set(self.dut.bus.dclk.i, 0)
        await ctx.delay(5e-6)

        ctx.set(self.dut.bus.dclk.i, 1)
        await ctx.delay(1e-6)

        ctx.set(self.dut.bus.data.i, 1)
        await ctx.delay(4e-6)

    async def write_nibble(self, ctx, nibble):
        await self.write_bit(ctx, nibble & 0x8)
        await self.write_bit(ctx, nibble & 0x4)
        await self.write_bit(ctx, nibble & 0x2)
        await self.write_bit(ctx, nibble & 0x1)
        await ctx.delay(10e-6)

    async def exchange_bits(self, ctx, out_bits):
        in_bits = []
        for out_bit in out_bits:
            await self.write_bit(ctx, out_bit)
            in_bit = await self.read_bit(ctx)
            in_bits.append(in_bit)
        return in_bits
