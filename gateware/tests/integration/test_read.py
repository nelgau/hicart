from amaranth import *
from amaranth.lib import wiring
from amaranth.sim import *
from amaranth_soc import wishbone

from hicart.interface import flash
from hicart.n64.cartbus import PISignature
from hicart.n64.pi import WishboneBridge
from hicart.soc.wishbone import DownConverter, WindowMapper
from hicart.sim.behavioral.pi import PIInitiatorDriver
from hicart.sim.behavioral.flash import FlashResponder
from hicart.sim.testcase import MultiProcessTestCase


class N64ReadTest(MultiProcessTestCase):

    class DUT(Elaboratable):

        def __init__(self):
            self.pi = PISignature.create()
            self.qspi = flash.Signature().create()

            self.bridge = WishboneBridge()

            self.flash_interface = flash.FlashWishboneInterface()
            self.flash_io = flash.SimFlashIO()

            self.translator = WindowMapper(sub_bus=self.flash_interface.bus,
                                            addr_width=23,
                                            base_addr=0x800000)

            self.down_converter = DownConverter(sub_bus=self.translator.bus,
                                            addr_width=22,
                                            data_width=16,
                                            granularity=8,
                                            features={"stall"})

        def elaborate(self, platform):
            m = Module()

            decoder = wishbone.Decoder(addr_width=31, data_width=16, granularity=8, features={"stall"})
            decoder.add(self.down_converter.bus, addr=0x10000000)

            m.submodules.bridge          = self.bridge
            m.submodules.decoder         = decoder
            m.submodules.flash_interface = self.flash_interface
            m.submodules.flash_io        = self.flash_io
            m.submodules.translator      = self.translator
            m.submodules.down_converter  = self.down_converter

            wiring.connect(m, self.bridge.pi, wiring.flipped(self.pi))
            wiring.connect(m, self.bridge.wb, decoder.bus)
            wiring.connect(m, self.flash_interface.qspi_ce, self.flash_io.qspi_ce)
            wiring.connect(m, self.flash_io.qspi, wiring.flipped(self.qspi))

            return m


    def test_read(self):
        dut = self.DUT()

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

        flash = FlashResponder(dut.qspi, flash_bytes)
        pi = PIInitiatorDriver(dut.pi)

        async def flash_process(ctx):
            await flash.run(ctx)

        async def pi_process(ctx):
            await pi.begin(ctx)

            for i in range(4):
                base_address = 0x10000000 + 4 * i
                check_reads(await pi.read_burst_slow(ctx, base_address, 2))

            check_reads(await pi.read_burst_fast(ctx, 0x10000000, 256))
            check_reads(await pi.read_burst_fast(ctx, 0x10000000, 256))

        traces = [
            dut.pi.ad.i,
            dut.pi.ad.o,
            dut.pi.ad.oe,
            dut.pi.ale_h.i,
            dut.pi.ale_l.i,
            dut.pi.read.i,
            dut.pi.write.i,

            dut.qspi.cs_n,
            dut.qspi.sck,
            dut.qspi.d.i,
            dut.qspi.d.o,
            dut.qspi.d.oe,

            dut.bridge.wb,

            dut.down_converter.bus,
            dut.translator.bus,
            dut.flash_interface.bus,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 80e6, domain="sync")
            sim.add_process(flash_process)
            sim.add_testbench(pi_process)
