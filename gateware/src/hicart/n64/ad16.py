from amaranth import *
from amaranth.hdl.ast import Fell
from amaranth.hdl.rec import Layout, DIR_FANIN, DIR_FANOUT
from amaranth.lib.cdc import FFSynchronizer

from hicart.n64.burst import BurstBus


ad16_layout = Layout.cast([
    ('ad', [
        ('i',    16, DIR_FANIN),
        ('o',    16, DIR_FANOUT),
        ('oe',   1,  DIR_FANOUT),
    ]),
    ('ale_h',    1,  DIR_FANIN),
    ('ale_l',    1,  DIR_FANIN),
    ('read',     1,  DIR_FANIN),
    ('write',    1,  DIR_FANIN),
    ('s_clk',    1,  DIR_FANIN),
    ('s_data', [
        ('i',    1,  DIR_FANIN),
        ('o',    1,  DIR_FANOUT),
        ('oe',   1,  DIR_FANOUT),
    ]),
    ('cic_dclk', 1, DIR_FANIN),
    ('cic_data', [
        ('i',    1, DIR_FANIN),
        ('o',    1, DIR_FANOUT),
        ('oe',   1, DIR_FANOUT)
    ]),
    ('reset',    1, DIR_FANIN),
    ('nmi',      1, DIR_FANIN),
])

class AD16(Record):
    def __init__(self, **kwargs):
        super().__init__(ad16_layout, **kwargs)


class AD16Interface(Elaboratable):
    def __init__(self):
        self.bus = BurstBus()
        self.ad16 = AD16()

        # Debugging

        self.late_block = Signal()
        self.late_read = Signal()

    def elaborate(self, platform):
        m = Module()

        ale_h_sync = Signal()
        ale_l_sync = Signal()
        read_sync = Signal()
        write_sync = Signal()
        ad_i_sync = Signal(16)

        m.submodules += FFSynchronizer( self.ad16.ale_h, ale_h_sync )
        m.submodules += FFSynchronizer( self.ad16.ale_l, ale_l_sync )
        m.submodules += FFSynchronizer( self.ad16.read,  read_sync  )
        m.submodules += FFSynchronizer( self.ad16.write, write_sync )
        m.submodules += FFSynchronizer( self.ad16.ad.i,  ad_i_sync, stages=4 )

        # Inputs: ad16.ale_l_sync, ad16.ale_h_sync, ad16.ad_i_sync 
        # Outputs: base, valid

        base = Signal(32)    
        offset = Signal(8)
        index = Signal()
        valid = Signal()

        with m.FSM() as fsm:                #   ALE_L       ALE_H
            with m.State("INIT"):           #   Inactive    Inactive
                with m.If(ale_l_sync):
                    m.next = "A"
            
            with m.State("A"):              #   Active      Inactive
                with m.If(~ale_l_sync):                    
                    m.next = "B"

            with m.State("B"):              #   Inactive    Inactive
                with m.If(ale_h_sync):
                    m.next = "C"

                    m.d.sync += base[14:30].eq(ad_i_sync)                

            with m.State("C"):              #   Inactive    Active
                with m.If(ale_l_sync):
                    m.next = "VALID"

                    m.d.sync += base[0:14].eq(ad_i_sync[2:16])
                    m.d.sync += offset.eq(0)
                    m.d.sync += index.eq(ad_i_sync[1])                

            with m.State("VALID"):          #   Active      Active
                with m.If(~ale_h_sync):
                    m.next = "A"

            m.d.comb += valid.eq(fsm.ongoing("VALID"))



        read_data = Signal(32)
        read_data_valid = Signal()
        wait_for_ack = Signal()

        op_begin = Signal()
        op_stall = Signal()
        op_read_data = Signal(32)
        op_read_data_valid = Signal()



        m.d.comb += op_begin            .eq(read_sync & ~read_data_valid & ~wait_for_ack)

        with m.If(op_begin & ~op_stall):
            m.d.sync += wait_for_ack    .eq(1)

        with m.If(Fell(read_sync)):
            m.d.sync += index.eq(index + 1)

            with m.If(index == 1):
                m.d.sync += [
                    offset              .eq(offset + 1),
                    read_data           .eq(0),
                    read_data_valid     .eq(0),
                    wait_for_ack        .eq(0),
                ]

            with m.If(~read_data_valid):
                m.d.comb += self.late_read  .eq(1)

        with m.If(wait_for_ack):
            with m.If(op_read_data_valid):
                m.d.sync += [
                    read_data           .eq(op_read_data),
                    read_data_valid     .eq(1),
                    wait_for_ack        .eq(0),
                ]

        m.d.sync += [
            self.ad16.ad.o      .eq(Mux(index, read_data[0:16], read_data[16:32])),
            self.ad16.ad.oe     .eq(read_sync & read_data_valid),
        ]






        with m.FSM() as fsm:

            m.d.comb += [                
                self.bus.blk                    .eq(~fsm.ongoing("IDLE")),
                op_stall                        .eq(~fsm.ongoing("BLOCK")),
            ]

            with m.State("IDLE"):
                with m.If(valid):
                    m.next = "BLOCK_BEGIN"
                    m.d.sync += self.bus.base   .eq(base)

            with m.State("BLOCK_BEGIN"):
                m.d.comb += self.bus.load       .eq(1)

                with m.If(~valid):
                    m.next = "IDLE"
                with m.If(~self.bus.blk_stall):
                    m.next = "BLOCK"

                with m.If(self.bus.blk_stall):
                    m.d.comb += self.late_block .eq(1)

            with m.State("BLOCK"):
                with m.If(~valid):
                    m.next = "IDLE"
                with m.Elif(op_begin):
                    m.next = "OP_BEGIN"
                    m.d.sync += self.bus.off    .eq(offset)
                    
            with m.State("OP_BEGIN"):
                m.d.comb += self.bus.cyc        .eq(1)
                m.d.comb += self.bus.stb        .eq(1)

                with m.If(~self.bus.stall):
                    m.next = "OP_WAIT"

            with m.State("OP_WAIT"):
                m.d.comb += self.bus.cyc        .eq(1)

                with m.If(self.bus.ack):            
                    m.next = "BLOCK"

                    m.d.comb += [
                        op_read_data            .eq(self.bus.dat_r),
                        op_read_data_valid      .eq(1),
                    ]

        return m
