from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.cdc import FFSynchronizer
from amaranth.lib.wiring import In, Out

from hicart.n64.cart import PISignature
from hicart.soc import seqbus


class PISeqBridge(wiring.Component):
    pi: Out(PISignature)
    seq: Out(seqbus.Signature(addr_width=31, data_width=16, granularity=8))

    def elaborate(self, platform):
        m = Module()

        # Synchronization

        ale_h_i_sync = Signal()
        ale_l_i_sync = Signal()
        read_i_sync = Signal()
        write_i_sync = Signal()
        ad_i_sync = Signal(16)

        m.submodules.sync_ale_h = FFSynchronizer(self.pi.ale_h, ale_h_i_sync)
        m.submodules.sync_ale_l = FFSynchronizer(self.pi.ale_l, ale_l_i_sync)
        m.submodules.sync_read  = FFSynchronizer(self.pi.read,  read_i_sync)
        m.submodules.sync_write = FFSynchronizer(self.pi.write, write_i_sync)
        m.submodules.sync_ad_i  = FFSynchronizer(self.pi.ad.i,  ad_i_sync, stages=4)

        # Address

        base_address = Signal(32)
        valid_address = Signal()

        with m.FSM():                       #   ALE_L       ALE_H
            with m.State("INIT"):           #   Inactive    Inactive
                with m.If(ale_l_i_sync):
                    m.next = "A"

            with m.State("A"):              #   Active      Inactive
                with m.If(~ale_l_i_sync):
                    m.next = "B"

            with m.State("B"):              #   Inactive    Inactive
                with m.If(ale_h_i_sync):
                    m.next = "C"
                    m.d.sync += base_address[16:32].eq(ad_i_sync)

            with m.State("C"):              #   Inactive    Active
                with m.If(ale_l_i_sync):
                    m.next = "VALID"
                    m.d.sync += base_address[0:16].eq(ad_i_sync[0:16])
                    m.d.sync += valid_address.eq(1)

            with m.State("VALID"):          #   Active      Active
                with m.If(~ale_h_i_sync):
                    m.d.sync += valid_address.eq(0)
                    m.next = "A"

        # Operations

        last_read_sync = Signal()
        read_op = Signal()

        m.d.sync += last_read_sync.eq(read_i_sync)
        m.d.comb += read_op.eq(read_i_sync & ~last_read_sync)

        with m.If(~read_i_sync):
            m.d.sync += self.pi.ad.oe.eq(0)

        # Seq bus

        current_address = Signal(32)

        m.d.comb += self.seq.adr.eq(current_address[1:32])
        m.d.comb += self.seq.sel.eq(Value.cast(1).replicate(2))

        with m.FSM():
            with m.State("IDLE"):
                with m.If(valid_address):
                    m.next = "CYCLE"
                    m.d.sync += self.seq.cyc.eq(1)
                    m.d.sync += current_address.eq(base_address)

            with m.State("CYCLE"):
                with m.If(~valid_address):
                    m.next = "IDLE"
                    m.d.sync += self.seq.cyc.eq(0)
                with m.Elif(read_op):
                    m.next = "READ"
                    m.d.sync += self.seq.stb.eq(1)
                    m.d.sync += self.seq.we.eq(0)

            with m.State("READ"):
                with m.If(self.seq.ack):
                    m.next = "CYCLE"
                    m.d.sync += self.seq.stb.eq(0)
                    m.d.sync += current_address.eq(current_address + 2)
                    m.d.sync += self.pi.ad.o.eq(self.seq.dat_r)
                    m.d.sync += self.pi.ad.oe.eq(1)

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

            word = ctx.get(self.pi.ad.o)
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

            word = ctx.get(self.pi.ad.o)
            ctx.set(self.pi.read, 0)
            await ctx.delay(416e-9)

            result.append((address, word))
            address += 2

        ctx.set(self.pi.ale_h, 0)
        await ctx.delay(32e-9)

        return result

    async def exit_cycle(self, ctx):
        ctx.set(self.pi.ale_l, 1)
        ctx.set(self.pi.ale_h, 0)
        await ctx.delay(1e-6)
