from amaranth import *
from amaranth.sim import *

from hicart.interface.hyperram import HyperRAMInterface
from hicart.test.pysim.utils import ModuleTestCase, sync_test_case


class TestHyperRAMInterface(ModuleTestCase):

    def instantiate_dut(self):
        # Create a record that recreates the layout of our RAM signals.
        self.ram_signals = Record([
            ("clk",   1),
            ("clkN",  1),
            ("dq",   [("i",  8), ("o",  8), ("oe", 1)]),
            ("rwds", [("i",  1), ("o",  1), ("oe", 1)]),
            ("cs",    1),
            ("reset", 1)
        ])

        # Create our HyperRAM interface...
        return HyperRAMInterface(bus=self.ram_signals)


    async def assert_clock_pulses(self, ctx, times=1):
        """ Function that asserts we get a specified number of clock pulses. """

        for _ in range(times):
            await ctx.tick()
            assert ctx.get(self.ram_signals.clk) == 1
            await ctx.tick()
            assert ctx.get(self.ram_signals.clk) == 0


    @sync_test_case
    async def test_register_write(self, ctx):

        # Before we transact, CS should be de-asserted, and RWDS and DQ should be undriven.
        await ctx.tick()
        assert ctx.get(self.ram_signals.cs) == 0
        assert ctx.get(self.ram_signals.dq.oe) == 0
        assert ctx.get(self.ram_signals.rwds.oe) == 0

        await ctx.tick().repeat(10)
        assert ctx.get(self.ram_signals.cs) == 0

        # Request a register write to ID register 0.
        ctx.set(self.dut.perform_write, 1)
        ctx.set(self.dut.register_space, 1)
        ctx.set(self.dut.address, 0x00BBCCDD)
        ctx.set(self.dut.start_transfer, 1)
        ctx.set(self.dut.final_word, 1)
        ctx.set(self.dut.write_data, 0xBEEF)

        # Simulate the RAM requesting a extended latency.
        ctx.set(self.ram_signals.rwds.i, 1)
        await ctx.tick()

        # Ensure that upon requesting, CS goes high, and our clock starts low.
        await ctx.tick()
        assert ctx.get(self.ram_signals.cs) == 1
        assert ctx.get(self.ram_signals.clk) == 0

        # Drop our "start request" line somewhere during the transaction;
        # so we don't immediately go into the next transfer.
        ctx.set(self.dut.start_transfer, 0)

        # We should then move to shifting out our first command word,
        # which means we're driving DQ with the first word of our command.
        await ctx.tick()
        assert ctx.get(self.ram_signals.cs) == 1
        assert ctx.get(self.ram_signals.clk) == 1
        assert ctx.get(self.ram_signals.dq.oe) == 1
        assert ctx.get(self.ram_signals.dq.o) == 0x60

        # Next, on the falling edge of our clock, the next byte should be presented.
        await ctx.tick()
        assert ctx.get(self.ram_signals.clk) == 0
        assert ctx.get(self.ram_signals.dq.o) == 0x17

        # This should continue until we've shifted out a full command.
        await ctx.tick()
        assert ctx.get(self.ram_signals.clk) == 1
        assert ctx.get(self.ram_signals.dq.o) == 0x79
        await ctx.tick()
        assert ctx.get(self.ram_signals.clk) == 0
        assert ctx.get(self.ram_signals.dq.o) == 0x9B
        await ctx.tick()
        assert ctx.get(self.ram_signals.clk) == 1
        assert ctx.get(self.ram_signals.dq.o) == 0x00
        await ctx.tick()
        assert ctx.get(self.ram_signals.clk) == 0
        assert ctx.get(self.ram_signals.dq.o) == 0x05

        # Check that we've been driving our output this whole time,
        # and haven't been driving RWDS.
        assert ctx.get(self.ram_signals.dq.oe) == 1
        assert ctx.get(self.ram_signals.rwds.oe) == 0
        await ctx.tick()

        # For a _register_ write, there shouldn't be latency period.
        # This means we should continue driving DQ...
        assert ctx.get(self.ram_signals.dq.oe) == 1
        assert ctx.get(self.ram_signals.rwds.oe) == 0

        assert ctx.get(self.ram_signals.clk) == 1
        assert ctx.get(self.ram_signals.dq.o) == 0xBE
        await ctx.tick()
        assert ctx.get(self.ram_signals.clk) == 0
        assert ctx.get(self.ram_signals.dq.o) == 0xEF


    @sync_test_case
    async def test_register_read(self, ctx):

        # Before we transact, CS should be de-asserted, and RWDS and DQ should be undriven.
        await ctx.tick()
        assert ctx.get(self.ram_signals.cs) == 0
        assert ctx.get(self.ram_signals.dq.oe) == 0
        assert ctx.get(self.ram_signals.rwds.oe) == 0

        await ctx.tick().repeat(10)
        assert ctx.get(self.ram_signals.cs) == 0

        # Request a register read of ID register 0.
        ctx.set(self.dut.perform_write, 0)
        ctx.set(self.dut.register_space, 1)
        ctx.set(self.dut.address, 0x00BBCCDD)
        ctx.set(self.dut.start_transfer, 1)
        ctx.set(self.dut.final_word, 1)

        # Simulate the RAM requesting a extended latency.
        ctx.set(self.ram_signals.rwds.i, 1)
        await ctx.tick()

        # Ensure that upon requesting, CS goes high, and our clock starts low.
        await ctx.tick()
        assert ctx.get(self.ram_signals.cs) == 1
        assert ctx.get(self.ram_signals.clk) == 0

        # Drop our "start request" line somewhere during the transaction;
        # so we don't immediately go into the next transfer.
        ctx.set(self.dut.start_transfer, 0)

        # We should then move to shifting out our first command word,
        # which means we're driving DQ with the first word of our command.
        await ctx.tick()
        assert ctx.get(self.ram_signals.cs) == 1
        assert ctx.get(self.ram_signals.clk) == 1
        assert ctx.get(self.ram_signals.dq.oe) == 1
        assert ctx.get(self.ram_signals.dq.o) == 0xe0

        # Next, on the falling edge of our clock, the next byte should be presented.
        await ctx.tick()
        assert ctx.get(self.ram_signals.clk) == 0
        assert ctx.get(self.ram_signals.dq.o) == 0x17

        # This should continue until we've shifted out a full command.
        await ctx.tick()
        assert ctx.get(self.ram_signals.clk) == 1
        assert ctx.get(self.ram_signals.dq.o) == 0x79
        await ctx.tick()
        assert ctx.get(self.ram_signals.clk) == 0
        assert ctx.get(self.ram_signals.dq.o) == 0x9B
        await ctx.tick()
        assert ctx.get(self.ram_signals.clk) == 1
        assert ctx.get(self.ram_signals.dq.o) == 0x00
        await ctx.tick()
        assert ctx.get(self.ram_signals.clk) == 0
        assert ctx.get(self.ram_signals.dq.o) == 0x05

        # Check that we've been driving our output this whole time,
        # and haven't been driving RWDS.
        assert ctx.get(self.ram_signals.dq.oe) == 1
        assert ctx.get(self.ram_signals.rwds.oe) == 0

        # Once we finish scanning out the word, we should stop driving
        # the data lines, and should finish two latency periods before
        # sending any more data.
        await ctx.tick()
        assert ctx.get(self.ram_signals.dq.oe) == 0
        assert ctx.get(self.ram_signals.rwds.oe) == 0
        assert ctx.get(self.ram_signals.clk) == 1

        # By this point, the RAM will drive RWDS low.
        ctx.set(self.ram_signals.rwds.i, 0)

        # Ensure the clock still ticking...
        await ctx.tick()
        assert ctx.get(self.ram_signals.clk) == 0

        # ... and remains so for the remainder of the latency period.
        await self.assert_clock_pulses(ctx, 7)

        # Now, shift in a pair of data words.
        ctx.set(self.ram_signals.dq.i, 0xCA)
        ctx.set(self.ram_signals.rwds.i, 1)
        await ctx.tick()
        ctx.set(self.ram_signals.dq.i, 0xFE)
        ctx.set(self.ram_signals.rwds.i, 0)
        await ctx.tick()

        # Once this finished, we should have a result on our data out.
        assert ctx.get(self.dut.read_data) == 0xCAFE
        assert ctx.get(self.dut.new_data_ready) == 1

        await ctx.tick()
        assert ctx.get(self.ram_signals.cs) == 0
        assert ctx.get(self.ram_signals.dq.oe) == 0
        assert ctx.get(self.ram_signals.rwds.oe) == 0

        # Ensure that our clock drops back to '0' during idle cycles.
        await ctx.tick().repeat(2)
        assert ctx.get(self.ram_signals.clk) == 0

        # TODO: test recovery time
