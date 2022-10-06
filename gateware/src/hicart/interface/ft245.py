from amaranth import *
from amaranth.hdl.rec import DIR_FANIN, DIR_FANOUT
from amaranth.lib.cdc import FFSynchronizer
from amaranth.lib.fifo import SyncFIFO

from hicart.soc.stream import BasicStream
from hicart.test.utils import ModuleTestCase, sync_test_case


class FT245Bus(Record):
    def __init__(self):
        super().__init__([
            ('d', [
                ('i',  8, DIR_FANIN),
                ('o',  8, DIR_FANOUT),
                ('oe', 1, DIR_FANOUT),
            ]),
            ('rxf', 1, DIR_FANIN),
            ('txe', 1, DIR_FANIN),
            ('rd',  1, DIR_FANOUT),
            ('wr',  1, DIR_FANOUT)
        ])


class FT245Interface(Elaboratable):
    WR_SETUP_CYCLES = 3
    WR_PULSE_CYCLES = 7
    RD_PULSE_CYCLES = 8
    RD_WAIT_CYCLES  = 5

    def __init__(self):     
        self.bus = FT245Bus()
        self.rx = BasicStream(8)
        self.tx = BasicStream(8)

        self._rx_fifo = SyncFIFO(width=8, depth=1)
        self._tx_fifo = SyncFIFO(width=8, depth=1)

    def elaborate(self, platform):
        m = Module()

        m.submodules.rx_fifo = self._rx_fifo
        m.submodules.tx_fifo = self._tx_fifo

        din = Signal(8)
        rxf = Signal()
        txe = Signal()

        m.submodules += [
            FFSynchronizer(self.bus.d.i, din, reset=0),
            FFSynchronizer(self.bus.rxf, rxf, reset=1),
            FFSynchronizer(self.bus.txe, txe, reset=1),
        ]

        count = Signal(8, reset=0)      # FIXME: Size this more appropriately later!
        rd = Signal(reset=1)
        wr = Signal(reset=1)

        m.d.sync += [
            self._rx_fifo.w_en.eq(0),
            self._tx_fifo.r_en.eq(0)
        ]

        with m.If(count > 0):
            m.d.sync += count.eq(count - 1)
        with m.Else():

            with m.FSM():

                with m.State("IDLE"):

                    m.d.sync += [
                        self.bus.d.oe           .eq(0),
                        rd                      .eq(1),
                        wr                      .eq(1),
                    ]

                    with m.If(self._rx_fifo.w_rdy & ~rxf):

                        m.next = "READ"
                        m.d.sync += [
                            count               .eq(self.RD_PULSE_CYCLES - 1),
                            rd                  .eq(0),         
                        ]

                    with m.Elif(self._tx_fifo.r_rdy & ~txe):

                        m.next = "WRITE"
                        m.d.sync += [
                            count               .eq(self.RD_PULSE_CYCLES - 1),
                            self._tx_fifo.r_en  .eq(1),
                            self.bus.d.o        .eq(self._tx_fifo.r_data),
                            self.bus.d.oe       .eq(1)
                        ]

                with m.State("READ"):

                    m.next = "IDLE"
                    m.d.sync += [
                        count                   .eq(self.RD_WAIT_CYCLES - 1),
                        self._rx_fifo.w_data    .eq(din),
                        self._rx_fifo.w_en      .eq(1),
                        rd                      .eq(1),                     
                        
                    ]

                with m.State("WRITE"):

                    m.next = "IDLE"
                    m.d.sync += [
                        count                   .eq(self.WR_PULSE_CYCLES - 1),
                        wr                      .eq(0),
                    ]

        m.d.comb += [
            self.bus.rd             .eq(rd),
            self.bus.wr             .eq(wr),
        ]

        m.d.comb += [
            self.rx.payload         .eq(self._rx_fifo.r_data),
            self.rx.valid           .eq(self._rx_fifo.r_rdy),
            self._rx_fifo.r_en      .eq(self.rx.ready),

            self._tx_fifo.w_data    .eq(self.tx.payload),
            self._tx_fifo.w_en      .eq(self.tx.valid),
            self.tx.ready           .eq(self._tx_fifo.w_rdy),
        ]

        return m


class FT245InterfaceTest(ModuleTestCase):
    FRAGMENT_UNDER_TEST = FT245Interface

    def instantiate_dut(self):
        dut = FT245Interface()

        dut.bus.rxf = Signal(reset=1)
        dut.bus.txe = Signal(reset=1)

        return dut

    def traces_of_interest(self):
        return [
            self.dut.bus.d.i,
            self.dut.bus.d.o,
            self.dut.bus.d.oe,
            self.dut.bus.rxf,
            self.dut.bus.txe,
            self.dut.bus.rd,
            self.dut.bus.wr,

            self.dut.rx.payload,
            self.dut.rx.valid,
            self.dut.rx.ready,

            self.dut.tx.payload,
            self.dut.tx.valid,
            self.dut.tx.ready,
        ]

    @sync_test_case
    def test_read(self):
        yield from self.advance_cycles(2)

        yield self.dut.bus.rxf.eq(0)
        yield from self.advance_cycles(2)

        yield from self.wait_until(~self.dut.bus.rd, timeout=20)
        yield from self.advance_cycles(2)

        yield self.dut.bus.rxf.eq(1)
        yield self.dut.bus.d.i.eq(0xA9)

        yield from self.wait_until( self.dut.bus.rd, timeout=20)
        yield from self.advance_cycles(2)
        yield self.dut.bus.rxf.eq(1)
        yield self.dut.bus.d.i.eq(0)

        self.assertEqual((yield self.dut.rx.payload), 0xA9)
        self.assertEqual((yield self.dut.rx.valid),   1)

        yield self.dut.rx.ready.eq(1)
        yield

        yield self.dut.rx.ready.eq(0)
        yield        

        self.assertEqual((yield self.dut.rx.valid), 0)

    @sync_test_case
    def test_write(self):
        yield from self.advance_cycles(2)

        self.assertEqual((yield self.dut.tx.ready), 1)

        yield self.dut.tx.payload.eq(0xBB)
        yield self.dut.tx.valid.eq(1)
        yield
        yield self.dut.tx.valid.eq(0)

        yield self.dut.bus.txe.eq(0)
            
        yield from self.wait_until(~self.dut.bus.wr, timeout=20)

        self.assertEqual((yield self.dut.bus.d.o),  0xBB)
        self.assertEqual((yield self.dut.bus.d.oe), 1)

        yield from self.wait_until( self.dut.bus.wr, timeout=20)

        self.assertEqual((yield self.dut.bus.d.oe), 0)
