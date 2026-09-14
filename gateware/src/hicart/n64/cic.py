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

from hicart.n64.cartbus import CICSignature


class Constants:
    RESET_ADDR = 0x00000000
    GPIO_ADDR = 0x00006000

    ROM_ADDR = 0x00000000
    ROM_SIZE = 0x1000

    RAM_ADDR = 0x00004000
    RAM_SIZE = 0x1000


class CIC(wiring.Component):
    bus:    Out(CICSignature)
    reset:  In(1)

    def __init__(self):
        super().__init__()

        # self.cpu = MinervaCPU(reset_address=Constants.RESET_ADDR)
        self.cpu = Minerva(reset_address=Constants.RESET_ADDR)

        self._arbiter = wishbone.Arbiter(addr_width=30, data_width=32, granularity=8, features={"cti", "bte"})
        self._decoder = wishbone.Decoder(addr_width=30, data_width=32, granularity=8, features={"cti", "bte"})

        self._arbiter.add(self.cpu.ibus)
        self._arbiter.add(self.cpu.dbus)

        self.rom = WishboneSRAM(size=Constants.ROM_SIZE, data_width=32, granularity=8, writable=False)
        self._decoder.add(self.rom.wb_bus, addr=Constants.ROM_ADDR, name="rom")

        self.ram = WishboneSRAM(size=Constants.RAM_SIZE, data_width=32, granularity=8)
        self._decoder.add(self.ram.wb_bus, addr=Constants.RAM_ADDR, name="ram")

        self._csr_decoder = csr.Decoder(addr_width=8, data_width=8)

        self.gpio = gpio.Peripheral(pin_count=2, addr_width=8, data_width=8, input_stages=2)
        self._csr_decoder.add(self.gpio.bus, name="gpio")

        self._csr_bridge = WishboneCSRBridge(self._csr_decoder.bus, data_width=32)

        self._decoder.add(self._csr_bridge.wb_bus, addr=Constants.GPIO_ADDR, name="csr")

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

        m.submodules.csr_bridge     = self._csr_bridge
        m.submodules.csr_decoder    = self._csr_decoder
        m.submodules.gpio           = self.gpio

        reset_sync  = Signal()
        m.d.comb += self.cpu.external_interrupt.eq(reset_sync)
        m.submodules += AsyncFFSynchronizer(self.reset, reset_sync)

        wiring.connect(m, self._arbiter.bus, self._decoder.bus)

        m.d.comb += [
            self.gpio.pins[0].i .eq( self.bus.dclk.i        ),
            self.gpio.pins[1].i .eq( self.bus.data.i        ),
            self.bus.data.o     .eq( self.gpio.pins[1].o    ),
            self.bus.data.oe    .eq( self.gpio.pins[1].oe   ),
        ]

        return m

