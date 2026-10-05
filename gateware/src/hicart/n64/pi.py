from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

from hicart.n64.cart import PISignature
from hicart.soc import seqbus
from hicart.utils.misc import FFDelay


class PISeqBridge(wiring.Component):

    # N.B. The control signals (e.g., ale_l, ale_h, read, write) need to be inverted!

    pi: Out(PISignature)
    seq: Out(seqbus.Signature(addr_width=31, data_width=16, granularity=8))

    # Delays for 80 Mhz

    READ_DELAY = 0
    WRITE_DELAY = 2 # ~25 ns
    OE_TIMEOUT = 7  # ~100 ns

    def elaborate(self, platform):
        m = Module()

        # Address

        base_address = Signal(32)
        valid_address = Signal()

        with m.FSM():                       #   ALE_L       ALE_H
            with m.State("INIT"):           #   Inactive    Inactive
                with m.If(self.pi.ale_l):
                    m.next = "A"

            with m.State("A"):              #   Active      Inactive
                with m.If(~self.pi.ale_l):
                    m.next = "B"

            with m.State("B"):              #   Inactive    Inactive
                with m.If(self.pi.ale_h):
                    m.next = "C"
                    m.d.sync += base_address[16:32].eq(self.pi.ad.i)

            with m.State("C"):              #   Inactive    Active
                with m.If(self.pi.ale_l):
                    m.next = "VALID"
                    m.d.sync += base_address[0:16].eq(self.pi.ad.i[0:16])
                    m.d.sync += valid_address.eq(1)

            with m.State("VALID"):          #   Active      Active
                with m.If(~self.pi.ale_h):
                    m.d.sync += valid_address.eq(0)
                    m.next = "A"

        # Operations

        read_delayed = Signal()
        write_delayed = Signal()

        last_read = Signal()
        last_write = Signal()

        do_read = Signal()
        do_write = Signal()

        m.submodules += [
            FFDelay(self.pi.read, read_delayed, stages=self.READ_DELAY),
            FFDelay(self.pi.write, write_delayed, stages=self.WRITE_DELAY),
        ]

        m.d.sync += last_read.eq(read_delayed)
        m.d.sync += last_write.eq(write_delayed)

        m.d.comb += do_read.eq(read_delayed & ~last_read)
        m.d.comb += do_write.eq(write_delayed & ~last_write)

        # Seq bus

        current_address = Signal(32)

        m.d.comb += self.seq.sel.eq(Const(1).replicate(2))
        m.d.comb += self.seq.adr.eq(current_address[1:32])
        m.d.comb += self.seq.dat_w.eq(self.pi.ad.i)

        with m.If(~self.seq.cyc):
            with m.If(valid_address):
                m.d.sync += self.seq.cyc.eq(1)
                m.d.sync += current_address.eq(base_address)

        with m.If(self.seq.cyc):
            with m.If(~valid_address):
                m.d.sync += self.seq.cyc.eq(0)
            with m.Elif(do_read | do_write):
                m.d.sync += self.seq.stb.eq(1)
                m.d.sync += self.seq.we.eq(do_write)

        with m.If(self.seq.ack | self.seq.err):
            m.d.sync += current_address.eq(current_address + 2)
            m.d.sync += self.seq.stb.eq(0)
            m.d.sync += self.seq.we.eq(0)

            with m.If(~self.seq.we):
                m.d.sync += self.pi.ad.o.eq(Mux(self.seq.ack, self.seq.dat_r, 0))
                m.d.sync += self.pi.ad.oe.eq(1)

        # Tri-state

        oe_counter = Signal(range(self.OE_TIMEOUT + 1))

        with m.If(oe_counter != 0):
            m.d.sync += oe_counter.eq(oe_counter - 1)
        with m.If(read_delayed):
            m.d.sync += oe_counter.eq(self.OE_TIMEOUT)

        with m.If(~valid_address | (oe_counter == 0)):
            m.d.sync += self.pi.ad.oe.eq(0)

        return m


class PIInitiatorDriver:

    # N.B. The control signals (e.g., ale_l, ale_h, read, write) need to be inverted!

    def __init__(self, pi):
        self.pi = pi

    async def begin(self, ctx):
        ctx.set(self.pi.ale_l, 1)
        ctx.set(self.pi.ale_h, 0)
        await ctx.delay(1e-6)

    async def read_burst_slow(self, ctx, start_address, word_count):
        ctx.set(self.pi.ale_l, 0)
        await ctx.delay(56e-9)
        ctx.set(self.pi.ad.i, (start_address >> 16) & 0xFFFF)
        await ctx.delay(56e-9)
        ctx.set(self.pi.ale_h, 1)
        await ctx.delay(56e-9)
        ctx.set(self.pi.ad.i, start_address & 0xFFFF)
        await ctx.delay(56e-9)
        ctx.set(self.pi.ale_l, 1)
        await ctx.delay(1040e-9)

        address = start_address
        result = []

        for i in range(word_count):
            ctx.set(self.pi.read, 1)
            await ctx.delay(304e-9)

            ad_o = ctx.get(self.pi.ad.o)
            ad_oe = ctx.get(self.pi.ad.oe)
            word = ad_o if ad_oe else 0

            ctx.set(self.pi.read, 0)
            await ctx.delay(64e-9)

            result.append((address, word))
            address += 2

        ctx.set(self.pi.ale_h, 0)
        await ctx.delay(2256e-9)

        return result

    async def read_burst_fast(self, ctx, start_address, word_count):

        # N.B., This does NOT model the behavior of splitting long bursts into subbursts of at most 256 words.

        ctx.set(self.pi.ale_l, 0)
        await ctx.delay(20e-9)
        ctx.set(self.pi.ad.i, (start_address >> 16) & 0xFFFF)
        await ctx.delay(92e-9)
        ctx.set(self.pi.ale_h, 1)
        await ctx.delay(20e-9)
        ctx.set(self.pi.ad.i, start_address & 0xFFFF)
        await ctx.delay(92e-9)
        ctx.set(self.pi.ale_l, 1)
        await ctx.delay(1044e-9)

        address = start_address
        result = []

        for i in range(word_count):
            ctx.set(self.pi.read, 1)
            await ctx.delay(304e-9)

            ad_o = ctx.get(self.pi.ad.o)
            ad_oe = ctx.get(self.pi.ad.oe)
            word = ad_o if ad_oe else 0

            ctx.set(self.pi.read, 0)
            await ctx.delay(64e-9)

            result.append((address, word))
            address += 2

        ctx.set(self.pi.ale_h, 0)
        await ctx.delay(32e-9)

        return result

    async def write_burst(self, ctx, start_address, values):
        if not values:
            raise ValueError("Burst must have at least one value");

        ctx.set(self.pi.ale_l, 0)
        await ctx.delay(20e-9)
        ctx.set(self.pi.ad.i, (start_address >> 16) & 0xFFFF)
        await ctx.delay(92e-9)
        ctx.set(self.pi.ale_h, 1)
        await ctx.delay(20e-9)
        ctx.set(self.pi.ad.i, start_address & 0xFFFF)
        await ctx.delay(92e-9)
        ctx.set(self.pi.ale_l, 1)
        await ctx.delay(1040e-9)

        for curr_val, next_val in zip(values, (*values, 0)):
            ctx.set(self.pi.ad.i, curr_val & 0xFFFF)
            ctx.set(self.pi.write, 1)
            await ctx.delay(304e-9)

            ctx.set(self.pi.write, 0)
            await ctx.delay(8e-9)

            ctx.set(self.pi.ad.i, next_val & 0xFFFF)
            await ctx.delay(56e-9)

        ctx.set(self.pi.ale_h, 0)
        await ctx.delay(32e-9)

    async def exit_cycle(self, ctx):
        ctx.set(self.pi.ale_l, 1)
        ctx.set(self.pi.ale_h, 0)
        await ctx.delay(1e-6)
