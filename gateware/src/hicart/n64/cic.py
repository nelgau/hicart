import struct

from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth.lib.cdc import FFSynchronizer, AsyncFFSynchronizer
from amaranth_soc import wishbone

from hicart.n64.cartbus import CICSignature
from hicart.soc.cpu.minerva  import MinervaCPU
from hicart.soc.periph.sram  import SRAMPeripheral
from hicart.soc.periph.gpio import GPIOPeripheral


class CIC(wiring.Component):
    bus:    Out(CICSignature)
    reset:  In(1)

    RESET_ADDR = 0x00000000
    GPIO_ADDR = 0x00006000

    ROM_ADDR = 0x00000000
    ROM_SIZE = 0x1000

    RAM_ADDR = 0x00004000
    RAM_SIZE = 0x1000

    def __init__(self):
        super().__init__()

        self._arbiter = wishbone.Arbiter(addr_width=30, data_width=32, granularity=8, features={"cti", "bte"})
        self._decoder = wishbone.Decoder(addr_width=30, data_width=32, granularity=8, features={"cti", "bte"})

        self.cpu = MinervaCPU(reset_address=CIC.RESET_ADDR)
        self._arbiter.add(self.cpu.ibus)
        self._arbiter.add(self.cpu.dbus)

        self.rom = SRAMPeripheral(size=CIC.ROM_SIZE, writable=False)
        self._decoder.add(self.rom.bus, addr=CIC.ROM_ADDR)

        self.ram = SRAMPeripheral(size=CIC.RAM_SIZE)
        self._decoder.add(self.ram.bus, addr=CIC.RAM_ADDR)

        self.gpio = GPIOPeripheral(data_width=8)
        self._decoder.add(self.gpio.bus, addr=CIC.GPIO_ADDR)

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

        reset_sync  = Signal()
        dclk_i_sync = Signal()
        data_i_sync = Signal()

        m.submodules += AsyncFFSynchronizer( self.reset,        reset_sync    )
        m.submodules += FFSynchronizer(      self.bus.dclk.i,   dclk_i_sync   )
        m.submodules += FFSynchronizer(      self.bus.data.i,   data_i_sync   )

        wiring.connect(m, self._arbiter.bus, self._decoder.bus)

        m.d.comb += [
            self.cpu.ip[0]      .eq( reset_sync      ),
            self.gpio.i[0]      .eq( dclk_i_sync     ),
            self.gpio.i[1]      .eq( data_i_sync     ),
            self.bus.data.o     .eq( self.gpio.o[1]  ),
            self.bus.data.oe    .eq( self.gpio.oe[1] ),
        ]

        return m
