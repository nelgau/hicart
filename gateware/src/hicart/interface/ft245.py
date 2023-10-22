from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.cdc import FFSynchronizer
from amaranth.lib.fifo import SyncFIFO
from amaranth.lib.wiring import In, Out, Signature

from hicart.soc.stream import BasicStream
from hicart.utils.plat import pin_signature


FT245Signature = Signature({
    "d":        Out(pin_signature(8, "io")),
    "rxf":      Out(pin_signature(1, "i")),
    "txe":      Out(pin_signature(1, "i")),
    "rd":       Out(pin_signature(1, "o")),
    "wr":       Out(pin_signature(1, "o")),
    "siwu":     Out(pin_signature(1, "o")),
    # Only used in synchronous mode.
    "clkout":   Out(pin_signature(1, "i")),
    "oe":       Out(pin_signature(1, "o")),
})


class FT245Interface(wiring.Component):
    bus: Out(FT245Signature)

    WR_SETUP_CYCLES = 3
    WR_PULSE_CYCLES = 7
    RD_PULSE_CYCLES = 8
    RD_WAIT_CYCLES  = 5

    def __init__(self):
        super().__init__()

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
            FFSynchronizer(self.bus.d.i,   din, reset=0),
            FFSynchronizer(self.bus.rxf.i, rxf, reset=1),
            FFSynchronizer(self.bus.txe.i, txe, reset=1),
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
            self.bus.rd.o           .eq(rd),
            self.bus.wr.o           .eq(wr),
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
