from amaranth import *
from amaranth.lib import wiring
from amaranth.sim import *
from amaranth_soc import wishbone

from hicart.interface.qspi_flash import QSPISignature, QSPIFlashWishboneInterface
from hicart.n64.cartbus import PISignature
from hicart.n64.pi import WishboneBridge
from hicart.soc.periph.sram  import SRAMPeripheral
from hicart.soc.wishbone import DownConverter, Translator
from hicart.test.pysim.driver.pi import PIInitiator
from hicart.test.pysim.emulator.qspi_flash import QSPIFlashEmulator
from hicart.test.pysim.testcase import MultiProcessTestCase


class DUT(Elaboratable):

    def __init__(self):
        self.pi = PISignature.create()
        self.qspi = QSPISignature().create()

        self.bridge = WishboneBridge()

        self.flash_interface = QSPIFlashWishboneInterface()

        self.translator = Translator(sub_bus=self.flash_interface.bus,
                                        base_addr=0x800000,
                                        addr_width=24,
                                        features={"stall"})

        self.down_converter = DownConverter(sub_bus=self.translator.bus,
                                        addr_width=23,
                                        data_width=16,
                                        granularity=8,
                                        features={"stall"})

    def elaborate(self, platform):
        m = Module()

        decoder = wishbone.Decoder(addr_width=31, data_width=16, granularity=8, features={"stall"})
        decoder.add(self.down_converter.bus, addr=0x10000000)

        m.submodules.bridge          = self.bridge
        m.submodules.decoder         = decoder
        # m.submodules.rom             = rom
        m.submodules.flash_interface = self.flash_interface
        m.submodules.translator      = self.translator
        m.submodules.down_converter  = self.down_converter

        wiring.connect(m, self.bridge.pi, wiring.flipped(self.pi))
        wiring.connect(m, self.bridge.wb, wiring.flipped(decoder.bus))
        wiring.connect(m, self.flash_interface.qspi, wiring.flipped(self.qspi))

        return m

    def ports(self):
        return [
            self.pi.ad.i,
            self.pi.ad.o,
            self.pi.ad.oe,
            self.pi.ale_h,
            self.pi.ale_l,
            self.pi.read,
            self.pi.write,

            self.qspi.sck,
            self.qspi.cs_n,
            self.qspi.d.i,
            self.qspi.d.o,
            self.qspi.d.oe,

            self.bridge.wb,

            self.down_converter.bus,
            self.translator.bus,
            self.flash_interface.bus,
        ]


class N64ReadTest(MultiProcessTestCase):

    def test_read(self):
        dut = DUT()

        with open("../roms/sm64.z64", "rb") as f:
            rom_bytes = list(f.read())

        flash_bytes = []
        flash_bytes += [0xFF] * 2**23
        # The ROM segment begins at offset 0x800000
        flash_bytes += rom_bytes

        def check_reads(reads):
            def assert_read(address, byte, position):
                offset = (address - 0x10000000) + 0x800000
                expected_byte = flash_bytes[offset]
                assert byte == expected_byte, f"Incorrect byte 0x{byte:02x} (!= 0x{expected_byte:02x}) " \
                        f"read ({position}) at address 0x{address:08x}, flash offset 0x{offset:06x}"

            for address, value in reads:
                assert_read(address + 0, value >> 8,    "HIGH")
                assert_read(address + 1, value & 0xFF,  "LOW")

        flash = QSPIFlashEmulator(dut.qspi, flash_bytes)
        pi = PIInitiator(dut.pi)

        def flash_process():
            yield Passive()
            yield from flash.emulate()

        def pi_process():
            yield from pi.begin()

            for i in range(4):
                base_address = 0x10000000 + 4 * i
                check_reads((yield from pi.read_burst_slow(base_address, 2)))

            check_reads((yield from pi.read_burst_fast(0x10000000, 256)))
            check_reads((yield from pi.read_burst_fast(0x10000000, 256)))

        with self.simulate(dut, traces=dut.ports()) as sim:
            sim.add_clock(1.0 / 80e6, domain='sync')
            sim.add_sync_process(flash_process)
            sim.add_process(pi_process)
