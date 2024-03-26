from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.cdc import FFSynchronizer
from amaranth.lib.fifo import SyncFIFOBuffered
from amaranth.lib.wiring import In, Out
from amaranth_soc import wishbone

from hicart.n64.cartbus import PISignature


class WishboneBridge(wiring.Component):
    pi:     Out(PISignature)
    wb:     Out(wishbone.Signature(addr_width=31, data_width=16, granularity=8, features={"stall"}))
    reset:  In(1)

    def elaborate(self, platform=None):
        m = Module()

        # Synchronization

        ale_h_i_sync = Signal()
        ale_l_i_sync = Signal()
        read_i_sync = Signal()
        write_i_sync = Signal()
        ad_i_sync = Signal(16)

        m.submodules.sync_ale_h = FFSynchronizer(self.pi.ale_h.i,   ale_h_i_sync)
        m.submodules.sync_ale_l = FFSynchronizer(self.pi.ale_l.i,   ale_l_i_sync)
        m.submodules.sync_read  = FFSynchronizer(self.pi.read.i,    read_i_sync)
        m.submodules.sync_write = FFSynchronizer(self.pi.write.i,   write_i_sync)
        m.submodules.sync_ad_i  = FFSynchronizer(self.pi.ad.i,      ad_i_sync, stages=4)

        # FIFOs

        read_fifo_reset = Signal()
        read_fifo_wait = Signal()

        m.submodules.read_fifo = read_fifo = ResetInserter(read_fifo_reset)(SyncFIFOBuffered(width=16, depth=4))

        # Address

        base_address = Signal(32)
        load_address = Signal()
        read_enabled = Signal()

        m.d.comb += read_fifo_reset.eq(0)
        m.d.sync += load_address.eq(0)

        with m.FSM() as fsm:                #   ALE_L       ALE_H
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
                    m.d.sync += load_address.eq(1)
                    m.d.sync += read_enabled.eq(1)

                    m.d.comb += read_fifo_reset.eq(1)
                    m.d.sync += read_fifo_wait.eq(0)

            with m.State("VALID"):          #   Active      Active
                with m.If(~ale_h_i_sync):
                    m.d.sync += read_enabled.eq(0)
                    m.next = "A"

        # Read FIFO

        last_read_sync = Signal()
        read_op = Signal()

        m.d.sync += last_read_sync.eq(read_i_sync)
        m.d.comb += read_op.eq(read_i_sync & ~last_read_sync)

        m.d.comb += read_fifo.r_en.eq(0)

        with m.If(read_op):
            with m.If(read_fifo.r_rdy):
                m.d.sync += self.pi.ad.o.eq(read_fifo.r_data)
                m.d.sync += self.pi.ad.oe.eq(1)
                m.d.comb += read_fifo.r_en.eq(1)
            with m.Else():
                m.d.sync += read_fifo_wait.eq(1)

        with m.If(read_fifo_wait):
            with m.If(read_fifo.r_rdy):
                m.d.sync += read_fifo_wait.eq(0)
                m.d.comb += read_fifo.r_en.eq(1)
                m.d.sync += self.pi.ad.o.eq(read_fifo.r_data)
                m.d.sync += self.pi.ad.oe.eq(1)

        with m.If(~read_i_sync):
            m.d.sync += self.pi.ad.oe.eq(0)

        # Wishbone bus

        current_address = Signal(32)

        m.d.comb += self.wb.adr.eq(current_address[1:32])
        m.d.comb += self.wb.sel.eq(Value.cast(1).replicate(2))

        with m.If(load_address):
            m.d.sync += current_address.eq(base_address)

        with m.If(~self.wb.cyc):
            with m.If(read_enabled & read_fifo.w_rdy):
                m.d.sync += self.wb.cyc.eq(1)
                m.d.sync += self.wb.stb.eq(1)
                m.d.sync += self.wb.we.eq(0)

        with m.If(self.wb.stb & ~self.wb.stall):
            m.d.sync += self.wb.stb.eq(0)

        with m.If(self.wb.ack):
            m.d.sync += self.wb.cyc.eq(0)
            m.d.sync += current_address.eq(current_address + 2)

        m.d.comb += [
            read_fifo.w_en.eq(self.wb.ack & ~self.wb.we),
            read_fifo.w_data.eq(self.wb.dat_r),
        ]

        return m
