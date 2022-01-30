import struct

from amaranth import *
from amaranth.lib.cdc import FFSynchronizer, AsyncFFSynchronizer

from amaranth_soc import wishbone

from lambdasoc.cpu.minerva  import MinervaCPU
from lambdasoc.periph.sram  import SRAMPeripheral

from ferk_cart.soc.gpio import GPIOPeripheral
from ferk_cart.test import *

class CIC(Elaboratable):
    def __init__(self):
        self.reset = Signal()
        self.data_clk = Signal()
        self.data_i = Signal()
        self.data_o = Signal()
        self.data_oe = Signal()

        reset_addr = 0x00000000
        
        rom_addr = 0x00000000
        rom_size = 0x1000
        
        ram_addr = 0x00004000
        ram_size = 0x1000

        gpio_addr = 0x00006000

        self._arbiter = wishbone.Arbiter(addr_width=30, data_width=32, granularity=8, features={"cti", "bte"})
        self._decoder = wishbone.Decoder(addr_width=30, data_width=32, granularity=8, features={"cti", "bte"})

        self.cpu = MinervaCPU(reset_address=reset_addr)
        self._arbiter.add(self.cpu.ibus)
        self._arbiter.add(self.cpu.dbus)

        self.rom = SRAMPeripheral(size=rom_size, writable=False)
        self._decoder.add(self.rom.bus, addr=rom_addr)

        self.ram = SRAMPeripheral(size=ram_size)
        self._decoder.add(self.ram.bus, addr=ram_addr)

        self.gpio = GPIOPeripheral(data_width=8)
        self._decoder.add(self.gpio.bus, addr=gpio_addr)

        self.memory_map = self._decoder.bus.memory_map

        with open("../firmware/firmware.bin", "rb") as f:
            rom_bytes = f.read()
            rom_data = [x[0] for x in struct.iter_unpack('<L', rom_bytes)]

        self.rom.init = rom_data

    def elaborate(self, platform):
        m = Module()

        m.submodules.arbiter = self._arbiter
        m.submodules.cpu     = self.cpu

        m.submodules.decoder = self._decoder
        m.submodules.rom     = self.rom
        m.submodules.ram     = self.ram
        m.submodules.gpio    = self.gpio

        reset_sync    = Signal()
        data_clk_sync = Signal()
        data_i_sync   = Signal()

        m.submodules += AsyncFFSynchronizer( self.reset,    reset_sync    )
        m.submodules += FFSynchronizer(      self.data_clk, data_clk_sync )
        m.submodules += FFSynchronizer(      self.data_i,   data_i_sync   )

        m.d.comb += [
            self._arbiter.bus.connect(self._decoder.bus),
            # self.cpu.ip.eq(self.intc.ip),

            self.cpu.ip[0].eq(reset_sync)
        ]

        m.d.comb += [
            self.gpio.i[0]  .eq( data_clk_sync   ),
            self.gpio.i[1]  .eq( data_i_sync     ),
            self.data_o     .eq( self.gpio.o[1]  ),
            self.data_oe    .eq( self.gpio.oe[1] ),
        ]

        return m

class CICTest(ModuleTestCase):
    FRAGMENT_UNDER_TEST = CIC

    def traces_of_interest(self):
        return [
            self.dut.reset,
            self.dut.data_clk,
            self.dut.data_i,
            self.dut.data_o,
            self.dut.data_oe,
        ]

    def initialize_signals(self):
        yield self.dut.reset    .eq(0)
        yield self.dut.data_clk .eq(1)
        yield self.dut.data_i   .eq(1)

    @sync_test_case
    def test_reset(self):    
        yield from self.wait(20e-6)

        # Preamble (from CIC)
        hello1 = yield from self.read_nibble()
        seed2  = yield from self.read_nibbles(2)
        
        yield self.dut.reset.eq(1)
        yield from self.advance_cycles(10)
        yield self.dut.reset.eq(0)

        yield from self.wait(20e-6)

        # Preamble (from CIC)
        hello2 = yield from self.read_nibble()
        seed2  = yield from self.read_nibbles(2)

        self.assertEqual(hello2, 0x1)
        self.assertEqual(seed2, [0xB, 0xD])

    @sync_test_case
    def test_output(self):
        yield from self.wait(50e-6)

        # Preamble (from CIC)

        hello = yield from self.read_nibble()
        seed  = yield from self.read_nibbles(6)

        self.assertEqual(hello, 0x1)
        self.assertEqual(seed, [0xB, 0xD, 0x3, 0x9, 0x3, 0xD])

        yield from self.wait(70e-6)
        yield from self.read_bit()

        checksum = yield from self.read_nibbles(16)

        self.assertEqual(checksum, [
            0x9, 0x0, 0x4, 0x0, 0xA, 0xE, 0xC, 0xB,
                0xF, 0xD, 0xA, 0xD, 0xB, 0x2, 0x6, 0x5])

        # Initial values (from PIF)

        yield from self.wait(20e-6)

        yield from self.write_nibble(0xA)
        yield from self.write_nibble(0x7)

        # Command 1 (from PIF)

        yield from self.wait(20e-6)
        yield from self.write_bit(0)
        yield from self.write_bit(0)
        yield from self.wait(200e-6)

        # Exchange 1 (Bidirectional)

        cmd1_in_bits = yield from self.exchange_bits([0, 1, 1, 0, 1, 1, 0])
        self.assertEqual(cmd1_in_bits, [1, 1, 1, 0, 1, 0, 1])

        # Command 2 (from PIF)

        yield from self.wait(20e-6)
        yield from self.write_bit(0)
        yield from self.write_bit(0)
        yield from self.wait(200e-6)

        # Exchange 2 (Bidirectional)

        cmd2_in_bits = yield from self.exchange_bits([
            1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1])
        self.assertEqual(cmd2_in_bits, [
            0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0])

    def read_bit(self):
        yield self.dut.data_clk.eq(0)
        yield from self.wait(5e-6)
        
        # As the signal is pulled high externally, the bit is low if oe & ~o.
        bit = yield (~self.dut.data_oe | self.dut.data_o)

        yield self.dut.data_clk.eq(1)
        yield from self.wait(5e-6)

        return bit

    def read_nibble(self):
        nibble = 0
        for _ in range(4):
            nibble <<= 1
            nibble |= yield from self.read_bit()

        yield from self.wait(10e-6)

        return nibble

    def read_nibbles(self, length):
        nibbles = []
        for _ in range(length):
            nibble = yield from self.read_nibble()
            nibbles.append(nibble)
        return nibbles

    def write_bit(self, bit):
        if bit == 0:
            yield self.dut.data_i.eq(0)

        yield self.dut.data_clk.eq(0)
        yield from self.wait(5e-6)
        
        yield self.dut.data_clk.eq(1)
        yield from self.wait(1e-6)
        
        yield self.dut.data_i.eq(1)
        yield from self.wait(4e-6)

    def write_nibble(self, nibble):
        yield from self.write_bit(nibble & 0x8)
        yield from self.write_bit(nibble & 0x4)
        yield from self.write_bit(nibble & 0x2)
        yield from self.write_bit(nibble & 0x1)

        yield from self.wait(10e-6)

    def exchange_bits(self, out_bits):
        in_bits = []
        for out_bit in out_bits:
            yield from self.write_bit(out_bit)
            in_bit = yield from self.read_bit()
            in_bits.append(in_bit)
        return in_bits
