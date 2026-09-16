from amaranth import *
from amaranth.sim import *


class FlashResponder:

    def __init__(self, qspi, data):
        self.qspi = qspi
        self.data = data

    async def run(self, ctx):
        while True:
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

    async def _read_spi(self, ctx, bit_count):
        result = 0

        for i in range(bit_count):
            aborted, qspi_do = await self._wait_for_read_clock(ctx)
            if aborted:
                return None

            result = (result << 1) | (qspi_do & 0x1)

        return result

    async def _read_qspi(self, ctx, nibble_count):
        result = 0

        for i in range(nibble_count):
            aborted, qspi_do = await self._wait_for_read_clock(ctx)
            if aborted:
                return None

            result = (result << 4) | (qspi_do & 0xF)

        return result

    async def _write_qspi(self, ctx, nibble_count, data):
        nibbles = []
        for i in range(nibble_count):
            nibbles.append(data & 0xF)
            data >>= 4

        for nibble in reversed(nibbles):
            aborted = await self._wait_for_write_clock(ctx)
            if aborted:
                return False

            ctx.set(self.qspi.d.i, nibble)

        return True

    async def _wait_for_cs(self, ctx):
        await ctx.negedge(self.qspi.cs_n)

    async def _wait_for_read_clock(self, ctx):
        cs_n, _, qspi_do = await (
            ctx.posedge(self.qspi.cs_n)
                    .posedge(self.qspi.sck)
                    .sample(self.qspi.d.o)
        )
        return (cs_n == 1, qspi_do)

    async def _wait_for_write_clock(self, ctx):
        cs_n, _ = await (
            ctx.posedge(self.qspi.cs_n)
                    .negedge(self.qspi.sck)
        )
        return (cs_n == 1)
