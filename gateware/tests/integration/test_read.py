from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out, flipped
from amaranth.sim import *

from hicart.host.subsystem import HostSubsystem
from hicart.controller import flash
from hicart.n64.cart import PISignature
from hicart.n64.pi import PIInitiatorDriver
from hicart.utils.sim import MultiProcessTestCase


class N64ReadTest(MultiProcessTestCase):

    class DUT(wiring.Component):
        pi: Out(PISignature)
        qspi: Out(flash.QSPISignature)

        def elaborate(self, platform):
            m = Module()

            flash_io = flash.SimFlashIO()
            host_subsystem = HostSubsystem()

            m.submodules.flash_io = flash_io
            m.submodules.host_subsystem = host_subsystem

            wiring.connect(m, host_subsystem.cart_pi, flipped(self.pi))
            wiring.connect(m, host_subsystem.flash, flash_io.bus)
            wiring.connect(m, flash_io.port, flipped(self.qspi))

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
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 80e6, domain="sync")
            sim.add_process(flash_process)
            sim.add_testbench(pi_process)
