from amaranth import *
from amaranth.sim import *
from amaranth_soc import wishbone

from hicart.interface.qspi_flash import QSPIBus, QSPIFlashWishboneInterface
from hicart.n64.ad16 import AD16
from hicart.n64.pi import PIWishboneInitiator
from hicart.soc.wishbone import DownConverter, Translator
from hicart.test.pysim.driver.ad16 import PIInitiator
from hicart.test.pysim.emulator.qspi_flash import QSPIFlashEmulator
from hicart.test.pysim.testcase import MultiProcessTestCase


class DUT(Elaboratable):

    def __init__(self):
        self.ad16 = AD16()
        self.qspi = QSPIBus()

        self.flash_interface = QSPIFlashWishboneInterface()

        self.translator = Translator(sub_bus=self.flash_interface.bus,
                                        base_addr=0x800000,
                                        addr_width=24,
                                        features={"stall"})

        self.down_converter = DownConverter(sub_bus=self.translator.bus,
                                        addr_width=22,
                                        data_width=32,
                                        granularity=8,
                                        features={"stall"})

    def elaborate(self, platform):
        m = Module()

        initiator = PIWishboneInitiator()
        
        decoder = wishbone.Decoder(addr_width=30, data_width=32, granularity=8, features={"stall"})
        decoder.add(self.down_converter.bus, addr=0x10000000)

        m.submodules.initiator       = initiator
        m.submodules.decoder         = decoder
        m.submodules.flash_interface = self.flash_interface
        m.submodules.translator      = self.translator
        m.submodules.down_converter  = self.down_converter

        m.d.comb += [
            initiator.ad16              .connect( self.ad16 ),
            initiator.bus               .connect( decoder.bus ),
            self.flash_interface.qspi   .connect( self.qspi ),
        ]

        return m

    def ports(self):
        return [
            self.ad16.ad.i,
            self.ad16.ad.o,
            self.ad16.ad.oe,
            self.ad16.ale_h,
            self.ad16.ale_l,
            self.ad16.read,
            self.ad16.write,
            self.ad16.reset,

            self.qspi.sck,
            self.qspi.cs_n,
            self.qspi.d.i,
            self.qspi.d.o,
            self.qspi.d.oe,

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

        flash = QSPIFlashEmulator(dut.qspi, flash_bytes)
        pi = PIInitiator(dut.ad16)

        def flash_process():
            yield Passive()
            yield from flash.emulate()

        def pi_process():
            yield from pi.begin()

            for i in range(4):
                base_address = 0x10000000 + 4 * i
                yield from pi.read_burst_slow(base_address, 2)

            yield from pi.read_burst_fast(0x10000000, 256)
            yield from pi.read_burst_fast(0x10000000, 256)

        with self.simulate(dut, traces=dut.ports()) as sim:
            sim.add_clock(1.0 / 60e6, domain='sync')
            sim.add_sync_process(flash_process)
            sim.add_process(pi_process)

    @staticmethod
    def _rom_bytes(data, data_width, byteorder):
        return [b for w in data for b in w.to_bytes(data_width, byteorder=byteorder)]
