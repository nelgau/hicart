import struct

from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth_soc import csr
from amaranth_soc import wishbone
from amaranth_soc.wishbone.sram import WishboneSRAM
from minerva.core import Minerva

from hicart.soc import csr_ext


class MCU(Elaboratable):

    class Constants:
        RESET_ADDR = 0x00000000
        CSR_ADDR = 0x00006000

        ROM_ADDR = 0x00000000
        ROM_SIZE = 0x1000

        RAM_ADDR = 0x00004000
        RAM_SIZE = 0x1000

    def __init__(self, *, mailbox_bus):
        self.mailbox_bus = mailbox_bus

        super().__init__()

        self.cpu = Minerva(reset_address=self.Constants.RESET_ADDR)

        self.arbiter = wishbone.Arbiter(addr_width=30, data_width=32, granularity=8, features={"cti", "bte"})
        self.decoder = wishbone.Decoder(addr_width=30, data_width=32, granularity=8, features={"cti", "bte"})

        self.arbiter.add(self.cpu.ibus)
        self.arbiter.add(self.cpu.dbus)

        # ROM

        self.rom = WishboneSRAM(size=self.Constants.ROM_SIZE, data_width=32, granularity=8, writable=False)

        # RAM

        self.ram = WishboneSRAM(size=self.Constants.RAM_SIZE, data_width=32, granularity=8)

        # CSR

        self.csr_decoder = csr.Decoder(addr_width=8, data_width=8)
        self.csr_decoder.add(mailbox_bus, name="mailbox")

        self.csr_bridge = csr_ext.WishboneCSRBridge(self.csr_decoder.bus, data_width=32, byteorder="little")

        # Decoder

        self.decoder.add(self.rom.wb_bus, addr=self.Constants.ROM_ADDR, name="rom")
        self.decoder.add(self.ram.wb_bus, addr=self.Constants.RAM_ADDR, name="ram")
        self.decoder.add(self.csr_bridge.wb_bus, addr=self.Constants.CSR_ADDR, name="csr")

        # Firmware

        with open("../firmware/mcu/build/mcu.bin", "rb") as f:
            rom_bytes = f.read()
            rom_data = [x[0] for x in struct.iter_unpack("<L", rom_bytes)]

        self.rom.init = rom_data

    def elaborate(self, platform):
        m = Module()

        m.submodules.cpu     = self.cpu
        m.submodules.arbiter = self.arbiter
        m.submodules.decoder = self.decoder

        m.submodules.rom     = self.rom
        m.submodules.ram     = self.ram

        m.submodules.csr_bridge     = self.csr_bridge
        m.submodules.csr_decoder    = self.csr_decoder

        wiring.connect(m, self.arbiter.bus, self.decoder.bus)

        return m
