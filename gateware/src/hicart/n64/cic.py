import struct

from amaranth import *
from amaranth.lib.cdc import FFSynchronizer, AsyncFFSynchronizer
from amaranth_soc import wishbone

from hicart.soc.cpu.minerva  import MinervaCPU
from hicart.soc.periph.sram  import SRAMPeripheral
from hicart.soc.periph.gpio import GPIOPeripheral


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
