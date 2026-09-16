from amaranth import *
from amaranth.sim import *


class QSPIFlashEmulator:

    def __init__(self, qspi, data):
        self.qspi = qspi
        self.data = data

    async def emulate(self, ctx):
        while True:
            ctx.set(self.qspi.d.i, 0)

            await self._wait_for_cs(ctx)

            command = await self._read_spi(ctx, 8)
            if command is None:
                continue

            assert command == 0xEB

            address = await self._read_qspi(ctx, 6)
            if address is None:
                continue

            mode = await self._read_qspi(ctx, 2)
            if mode is None:
                continue

            assert mode == 0xF0

            dummy = await self._read_qspi(ctx, 4)
            if dummy is None:
                continue

            while True:
                data = self._load_data(address)
                bursting = await self._write_qspi(ctx, 2, data)
                if not bursting:
                    break
                address += 1

    def _load_data(self, address):
        if address < len(self.data):
            return self.data[address]
        else:
            return 0xFF

    async def _wait_for_cs(self, ctx):
        while ctx.get(self.qspi.cs_n):
            await ctx.tick()

    async def _read_spi(self, ctx, bit_count):
        result = 0

        for i in range(bit_count):
            aborted = await self._wait_for_next_clock(ctx)
            if aborted:
                return None

            bit = ctx.get(self.qspi.d.o[0])
            result = (result << 1) | bit
            await ctx.tick()

        return result

    async def _read_qspi(self, ctx, nibble_count):
        result = 0

        for i in range(nibble_count):
            aborted = await self._wait_for_next_clock(ctx)
            if aborted:
                return None

            nibble = ctx.get(self.qspi.d.o)
            result = (result << 4) | nibble
            await ctx.tick()

        return result

    async def _write_qspi(self, ctx, nibble_count, data):
        nibbles = []
        for i in range(nibble_count):
            nibbles.append(data & 0xF)
            data >>= 4

        for nibble in reversed(nibbles):
            aborted = await self._wait_for_next_clock(ctx)
            if aborted:
                return False

            ctx.set(self.qspi.d.i, nibble)
            await ctx.tick()

        return True

    async def _wait_for_next_clock(self, ctx):
        while True:
            if ctx.get(self.qspi.cs_n):
                return True

            if ctx.get(self.qspi.sck):
                return False

            await ctx.tick()
