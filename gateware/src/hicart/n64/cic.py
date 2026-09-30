from enum import IntEnum
import struct

from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth.lib.cdc import AsyncFFSynchronizer
from amaranth_soc import csr
from amaranth_soc import gpio
from amaranth_soc.csr.wishbone import WishboneCSRBridge
from amaranth_soc import wishbone
from amaranth_soc.wishbone.sram import WishboneSRAM
from minerva.core import Minerva

from hicart.n64.cart import CICSignature, CtlSignature


class CIC(wiring.Component):
    bus:    Out(CICSignature)
    ctl:    Out(CtlSignature)

    class Constants:
        RESET_ADDR = 0x00000000
        GPIO_ADDR = 0x00006000

        ROM_ADDR = 0x00000000
        ROM_SIZE = 0x1000

        RAM_ADDR = 0x00004000
        RAM_SIZE = 0x1000

    def __init__(self):
        super().__init__()

        self.cpu = Minerva(reset_address=self.Constants.RESET_ADDR)

        self._arbiter = wishbone.Arbiter(addr_width=30, data_width=32, granularity=8, features={"cti", "bte"})
        self._decoder = wishbone.Decoder(addr_width=30, data_width=32, granularity=8, features={"cti", "bte"})

        self._arbiter.add(self.cpu.ibus)
        self._arbiter.add(self.cpu.dbus)

        self.rom = WishboneSRAM(size=self.Constants.ROM_SIZE, data_width=32, granularity=8, writable=False)
        self._decoder.add(self.rom.wb_bus, addr=self.Constants.ROM_ADDR, name="rom")

        self.ram = WishboneSRAM(size=self.Constants.RAM_SIZE, data_width=32, granularity=8)
        self._decoder.add(self.ram.wb_bus, addr=self.Constants.RAM_ADDR, name="ram")

        self._csr_decoder = csr.Decoder(addr_width=8, data_width=8)

        self.gpio = gpio.Peripheral(pin_count=2, addr_width=8, data_width=8, input_stages=2)
        self._csr_decoder.add(self.gpio.bus, name="gpio")

        self._csr_bridge = WishboneCSRBridge(self._csr_decoder.bus, data_width=32)

        self._decoder.add(self._csr_bridge.wb_bus, addr=self.Constants.GPIO_ADDR, name="csr")

        with open("../firmware/firmware.bin", "rb") as f:
            rom_bytes = f.read()
            rom_data = [x[0] for x in struct.iter_unpack("<L", rom_bytes)]

        self.rom.init = rom_data

    def elaborate(self, platform):
        m = Module()

        m.submodules.arbiter = self._arbiter
        m.submodules.cpu     = self.cpu

        m.submodules.decoder = self._decoder
        m.submodules.rom     = self.rom
        m.submodules.ram     = self.ram

        m.submodules.csr_bridge     = self._csr_bridge
        m.submodules.csr_decoder    = self._csr_decoder
        m.submodules.gpio           = self.gpio

        reset_sync  = Signal()
        m.d.comb += self.cpu.external_interrupt.eq(reset_sync)
        m.submodules += AsyncFFSynchronizer(self.ctl.reset, reset_sync)

        wiring.connect(m, self._arbiter.bus, self._decoder.bus)

        m.d.comb += [
            self.gpio.pins[0].i .eq( self.bus.dclk          ),
            self.gpio.pins[1].i .eq( self.bus.data.i        ),
            self.bus.data.o     .eq( self.gpio.pins[1].o    ),
            self.bus.data.oe    .eq( self.gpio.pins[1].oe   ),
        ]

        return m


class CICDriver:

    class Command(IntEnum):
        COMPARE = 0
        DIE = 1
        CIC6105 = 2
        RESET = 3

    def __init__(self, bus, reset_signal):
        self.bus = bus
        self.reset_signal = reset_signal

    async def begin(self, ctx):
        ctx.set(self.reset_signal, 0)
        ctx.set(self.bus.dclk, 1)
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
        ctx.set(self.bus.dclk, 0)
        await ctx.delay(5e-6)

        # As the signal is pulled high externally, the bit is low if oe & ~o.
        bit = ctx.get(~self.bus.data.oe | self.bus.data.o)

        ctx.set(self.bus.dclk, 1)
        await ctx.delay(5e-6)

        return bit

    async def _read_nibble(self, ctx):
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

        ctx.set(self.bus.dclk, 0)
        await ctx.delay(5e-6)

        ctx.set(self.bus.dclk, 1)
        await ctx.delay(1e-6)

        ctx.set(self.bus.data.i, 1)
        await ctx.delay(4e-6)

    async def _write_nibble(self, ctx, nibble):
        await self._write_bit(ctx, nibble & 0x8)
        await self._write_bit(ctx, nibble & 0x4)
        await self._write_bit(ctx, nibble & 0x2)
        await self._write_bit(ctx, nibble & 0x1)
        await ctx.delay(10e-6)

