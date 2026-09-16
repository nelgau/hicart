from amaranth import *
from amaranth.lib import wiring
from amaranth.sim import *
from amaranth_soc import wishbone
from amaranth_soc.wishbone.sram import WishboneSRAM

from hicart.n64.cartbus import PISignature
from hicart.n64.pi import WishboneBridge
from hicart.sim.testcase import MultiProcessTestCase


class WishboneBridgeTest(MultiProcessTestCase):

    class DUT(Elaboratable):

        ROM_DATA = [
            0x3210,     # 0x1000000
            0xBA98,
            0xBABE,
            0xBEEF,
        ]

        def __init__(self):
            self.pi = PISignature.create()

        def elaborate(self, platform):
            m = Module()

            self.decoder = wishbone.Decoder(addr_width=31, data_width=16, granularity=8, features={"stall"})

            self.rom = WishboneSRAM(size=16, data_width=16, granularity=8, writable=False)
            self.decoder.add(self.rom.wb_bus, addr=0x10000000)

            self.rom.init = self.ROM_DATA

            self.initiator = WishboneBridge()

            m.submodules.initiator = self.initiator
            m.submodules.decoder   = self.decoder
            m.submodules.rom       = self.rom

            wiring.connect(m, self.initiator.pi, wiring.flipped(self.pi))
            wiring.connect(m, self.initiator.wb, self.decoder.bus)

            return m


    def test_basic(self):
        dut = self.DUT()

        async def testbench(ctx):
            # Ale_l is active in idle state
            ctx.set(dut.pi.ale_l.i, 1)
            ctx.set(dut.pi.ale_h.i, 0)
            await ctx.tick().repeat(6)

            # Latch address

            ctx.set(dut.pi.ale_l.i, 0)
            await ctx.tick().repeat(2)
            ctx.set(dut.pi.ad.i, 0x1000)
            await ctx.tick().repeat(2)
            ctx.set(dut.pi.ale_h.i, 1)
            await ctx.tick().repeat(2)
            ctx.set(dut.pi.ad.i, 0x0002)
            await ctx.tick().repeat(2)
            ctx.set(dut.pi.ale_l.i, 1)
            await ctx.tick().repeat(8)

            # Read

            for i in range(3):
                ctx.set(dut.pi.read.i, 1)
                await ctx.tick().repeat(6)

                assert ctx.get(dut.pi.ad.o) == dut.ROM_DATA[i + 1]
                assert ctx.get(dut.pi.ad.oe) == 1

                ctx.set(dut.pi.read.i, 0)
                await ctx.tick().repeat(6)

                assert ctx.get(dut.pi.ad.oe) == 0

        traces = [
            dut.pi.ad.i,
            dut.pi.ad.o,
            dut.pi.ad.oe,
            dut.pi.ale_h.i,
            dut.pi.ale_l.i,
            dut.pi.read.i,
            dut.pi.write.i
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 80e6, domain="sync")
            sim.add_testbench(testbench)
