from dataclasses import dataclass
import struct
import typing

from amaranth import *
from amaranth.lib import wiring
from amaranth_soc import csr, wishbone
from amaranth_soc.wishbone.sram import WishboneSRAM
from minerva.core import Minerva

from hicart.soc import csr_ext



ROM_BASE    = 0x0000_0000
RAM_BASE    = 0x4000_0000
WB_BASE     = 0x8000_0000
CSR_BASE    = 0xC000_0000
REGION_SIZE = 0x4000_0000


@dataclass
class CpuBlockConfig:
    rom_size: int
    ram_size: int

    @dataclass(frozen=True)
    class Window:
        sub_bus: typing.Any
        name: str | None
        addr: int | None

    def __post_init__(self):
        self._wb_windows = []
        self._csr_windows = []

    @property
    def wb_windows(self):
        return self._wb_windows

    @property
    def csr_windows(self):
        return self._csr_windows

    def add_wishbone(self, sub_bus, *, name=None, addr=None):
        if addr is not None and (addr < WB_BASE or addr > WB_BASE + REGION_SIZE):
            raise ValueError("Address 0x{addr:08x} is outside Wishbone region")
        self.wb_windows.append(self.Window(sub_bus=sub_bus, name=name, addr=addr))

    def add_csr(self, sub_bus, *, name=None, addr=None):
        if addr is not None and (addr < CSR_BASE or addr > CSR_BASE + REGION_SIZE):
            raise ValueError("Address 0x{addr:08x} is outside CSR region")
        self.csr_windows.append(self.Window(sub_bus=sub_bus, name=name, addr=addr))


class CpuBlock(Elaboratable):

    def __init__(self, config, *, firmware=None, allow_empty_rom=False):
        self._config = config
        self._firmware = None
        self._allow_empty_rom = allow_empty_rom
        super().__init__()

        if firmware is not None:
            self.firmware = firmware

        self._csr_decoders = []
        self._csr_bridges = []

        # Core

        self._core = Minerva(reset_address=ROM_BASE)

        self._arbiter = wishbone.Arbiter(addr_width=30, data_width=32, granularity=8, features={"cti", "bte"})
        self._decoder = wishbone.Decoder(addr_width=30, data_width=32, granularity=8, features={"cti", "bte"})

        self._arbiter.add(self._core.ibus)
        self._arbiter.add(self._core.dbus)

        # Memory

        self._rom = WishboneSRAM(size=self._config.rom_size, data_width=32, granularity=8, writable=False)
        self._ram = WishboneSRAM(size=self._config.ram_size, data_width=32, granularity=8)

        self._decoder.add(self._rom.wb_bus, addr=ROM_BASE, name="rom")
        self._decoder.add(self._ram.wb_bus, addr=RAM_BASE, name="ram")

        # Wishbone windows

        for window in self._config.wb_windows:
            self._decoder.add(window.sub_bus, name=window.name, addr=window.addr)

        # CSR windows

        for window in self._config.csr_windows:
            csr_decoder = csr.Decoder(addr_width=8, data_width=8)
            csr_decoder.add(window.sub_bus)

            csr_bridge = csr_ext.WishboneCSRBridge(csr_decoder.bus, data_width=32, byteorder="little")

            self._decoder.add(csr_bridge.wb_bus, name=window.name, addr=window.addr)

            self._csr_decoders.append(csr_decoder)
            self._csr_bridges.append(csr_bridge)

    @property
    def firmware(self):
        return self._firmware

    @firmware.setter
    def firmware(self, data):
        if len(data) > self._config.rom_size:
            raise ValueError(f"Firmware is {len(data)} bytes; ROM holds {self._config.rom_size} bytes")
        self._firmware = data

    @property
    def memory_map(self):
        return self._decoder.bus.memory_map

    def elaborate(self, platform):
        m = Module()

        m.submodules.core = self._core
        m.submodules.abiter = self._arbiter
        m.submodules.decoder = self._decoder

        wiring.connect(m, self._arbiter.bus, self._decoder.bus)

        m.submodules.rom = self._rom
        m.submodules.ram = self._ram

        for i, csr_decoder in enumerate(self._csr_decoders):
            m.submodules[f"csr_decoder_{i}"] = csr_decoder

        for i, csr_bridge in enumerate(self._csr_bridges):
            m.submodules[f"csr_bridge_{i}"] = csr_bridge

        if self._firmware is not None:
            # Unpack into words, litte-endian
            rom_words = [x[0] for x in struct.iter_unpack("<L", self._firmware)]
            self._rom.init = rom_words
        elif not self._allow_empty_rom:
            raise ValueError("Cannot elaborate without firmware")

        return m
