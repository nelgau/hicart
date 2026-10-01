from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out, flipped
from amaranth.sim import *
from amaranth_soc import wishbone
from amaranth_soc.csr.wishbone import WishboneCSRBridge

from hicart.soc.wishbone import WishboneClassicDriver
from hicart.sys.mailbox import CommandMailbox
from hicart.utils.sim import MultiProcessTestCase, in_domain


class CommandMailboxTest(MultiProcessTestCase):

    class DUT(wiring.Component):

        def __init__(self):
            self.mailbox = CommandMailbox(sys_domain="sys")

            self.host_bridge = WishboneCSRBridge(self.mailbox.host_bus, data_width=16)
            self.host_decoder = wishbone.Decoder(addr_width=31, data_width=16, granularity=8)
            self.host_decoder.add(self.host_bridge.wb_bus, addr=0x0)

            self.sys_bridge = DomainRenamer("sys")(WishboneCSRBridge(self.mailbox.sys_bus, data_width=32))
            self.sys_decoder = DomainRenamer("sys")(wishbone.Decoder(addr_width=30, data_width=32, granularity=8))
            self.sys_decoder.add(self.sys_bridge.wb_bus, addr=0x0)

            super().__init__({
                "host_bus": In(wishbone.Signature(addr_width=31, data_width=16, granularity=8)),
                "sys_bus": In(wishbone.Signature(addr_width=30, data_width=32, granularity=8)),
            })
            self.host_bus.memory_map = self.host_decoder.bus.memory_map
            self.sys_bus.memory_map = self.sys_decoder.bus.memory_map

        def elaborate(self, platform):
            m = Module()

            m.submodules.mailbox = self.mailbox
            m.submodules.host_bridge = self.host_bridge
            m.submodules.host_decoder = self.host_decoder
            m.submodules.sys_bridge = self.sys_bridge
            m.submodules.sys_decoder = self.sys_decoder

            wiring.connect(m, flipped(self.host_bus), self.host_decoder.bus)
            wiring.connect(m, flipped(self.sys_bus), self.sys_decoder.bus)

            return m

    def test_basic(self):
        dut = self.DUT()

        host_driver = WishboneClassicDriver(dut.host_bus)
        sys_driver = WishboneClassicDriver(dut.sys_bus)

        async def host_testbench(ctx):
            await host_driver.begin(ctx)
            await ctx.tick()

            # Arg 1
            await host_driver.write_once(ctx, 0x4, 0x0012)
            await host_driver.write_once(ctx, 0x5, 0x0034)

            # Arg 2
            await host_driver.write_once(ctx, 0x6, 0x0056)
            await host_driver.write_once(ctx, 0x7, 0x0078)

            # Command
            await host_driver.write_once(ctx, 0x2, 0x0000)
            await host_driver.write_once(ctx, 0x3, 0xFACE)

            await ctx.tick().repeat(10)

            result_low = None
            result_high = None

            while True:
                result_low = await host_driver.read_once(ctx, 0x0)
                _ = await host_driver.read_once(ctx, 0x1)

                if not result_low & 0x1:
                    break

            # Check for error bit
            assert result_low & 0x2

            # Result
            result_low = await host_driver.read_once(ctx, 0x8)
            result_high = await host_driver.read_once(ctx, 0x9)

            assert result_low == 0xCAFE
            assert result_high == 0x1234

            await ctx.tick()

        async def sys_testbench(ctx):
            await sys_driver.begin(ctx)
            await ctx.tick()

            while True:
                result = await sys_driver.read_once(ctx, 0x0)
                if result & 0x1:
                    break

            assert await sys_driver.read_once(ctx, 0x1) == 0xFACE0000   # Command
            assert await sys_driver.read_once(ctx, 0x2) == 0x00340012   # Arg 1
            assert await sys_driver.read_once(ctx, 0x3) == 0x00780056   # Arg 2

            await ctx.tick()

            # Result
            await sys_driver.write_once(ctx, 0x4, 0x1234CAFE)

            # Done with error bit set
            await sys_driver.write_once(ctx, 0x0, 0x0002)

            await ctx.tick()

        traces = [
            dut.host_bus
        ]

        with self.simulate(dut, traces=traces) as sim:
            sim.add_clock(1.0 / 100e6, domain="sync")
            sim.add_clock(1.0 / 40e6, domain="sys")
            sim.add_testbench(host_testbench)
            sim.add_testbench(in_domain(sys_testbench, domain="sys"))
