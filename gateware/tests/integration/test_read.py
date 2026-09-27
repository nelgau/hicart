from amaranth import *
from amaranth.lib import wiring
from amaranth.sim import *
from amaranth_soc import wishbone

from hicart.controller import flash
from hicart.n64.cart import PISignature
from hicart.n64.pi import WishboneBridge, PIInitiatorDriver
from hicart.soc.wishbone import WindowMapper
from hicart.sim.testcase import MultiProcessTestCase


class N64ReadTest(MultiProcessTestCase):

    class DUT(Elaboratable):

        def __init__(self):
            self.pi = PISignature.create()
            self.qspi = flash.QSPISignature.create()

            self.bridge = WishboneBridge()

            self.flash_ctrl = flash.WishboneFlashController(data_width=16)
            self.flash_io = flash.SimFlashIO()

            self.mapper = WindowMapper(self.flash_ctrl.wb,
                                       addr_width=22,
                                       base_addr=0x800000)

        def elaborate(self, platform):
            m = Module()

            decoder = wishbone.Decoder(addr_width=31, data_width=16, granularity=8, features={"stall"})
            decoder.add(self.mapper.bus, addr=0x10000000)

            m.submodules.bridge     = self.bridge
            m.submodules.decoder    = decoder
            m.submodules.flash_ctrl = self.flash_ctrl
            m.submodules.flash_io   = self.flash_io
            m.submodules.mapper     = self.mapper

            wiring.connect(m, self.bridge.pi, wiring.flipped(self.pi))
            wiring.connect(m, self.bridge.wb, decoder.bus)
            wiring.connect(m, self.flash_ctrl.bus, self.flash_io.bus)
            wiring.connect(m, self.flash_io.port, wiring.flipped(self.qspi))

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

        flr = flash.FlashResponder(dut.qspi, flash_bytes)
        pi = PIInitiatorDriver(dut.pi)

        async def flash_process(ctx):
            await flr.run(ctx)

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
            dut.pi.ale_h,
            dut.pi.ale_l,
            dut.pi.read,
            dut.pi.write,

            dut.qspi.cs_n,
            dut.qspi.sck,
            dut.qspi.d.i,
            dut.qspi.d.o,
            dut.qspi.d.oe,

            dut.bridge.wb,
            dut.mapper.bus,
            dut.flash_ctrl.wb,
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 80e6, domain="sync")
            sim.add_process(flash_process)
            sim.add_testbench(pi_process)
