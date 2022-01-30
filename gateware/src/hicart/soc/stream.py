from amaranth import *
from amaranth.hdl.rec import DIR_FANIN, DIR_FANOUT

from hicart.test import *


class BasicStream(Record):

    def __init__(self, width):
        super().__init__([
            ('payload',     width,  DIR_FANOUT),
            ('valid',       1,      DIR_FANOUT),
            ('ready',       1,      DIR_FANIN)
        ])

class ByteDownConverter(Elaboratable):

    def __init__(self, byte_width):
        self.byte_width = byte_width

        self.source = BasicStream(width=8 * byte_width)
        self.sink   = BasicStream(width=8)

    def elaborate(self, platform):
        m = Module()

        data_shift = Signal.like(self.source.payload)
        bytes_to_send = Signal(range(0, self.byte_width + 1))

        m.d.comb += [
            self.sink.payload.eq(data_shift[0:8])
        ]

        with m.FSM():

            with m.State("IDLE"):
                m.d.comb += self.source.ready.eq(1)

                # Once we get a send request, fill in our shift register, and start shifting.
                with m.If(self.source.valid):
                    m.d.sync += [
                        data_shift         .eq(self.source.payload),
                        bytes_to_send      .eq(self.byte_width - 1),
                    ]
                    m.next = "RUN"

            with m.State("RUN"):
                m.d.comb += self.sink.valid.eq(1)

                # Once the UART is accepting our input...
                with m.If(self.sink.ready):

                    # ... if we have bytes left to send, move to the next one.
                    with m.If(bytes_to_send > 0):
                        m.d.sync += [
                            bytes_to_send .eq(bytes_to_send - 1),
                            data_shift    .eq(data_shift[8:]),
                        ]

                    # Otherwise, complete the frame.
                    with m.Else():
                        m.d.comb += self.source.ready.eq(1)

                        # If we still have data to send, move to the next byte...
                        with m.If(self.source.valid):
                            m.d.sync += [
                                bytes_to_send      .eq(self.byte_width - 1),
                                data_shift         .eq(self.source.payload),
                            ]

                        # ... otherwise, move to our idle state.
                        with m.Else():
                            m.next = "IDLE"

        return m

class ByteDownConverterTest(ModuleTestCase):
    FRAGMENT_UNDER_TEST = ByteDownConverter
    FRAGMENT_ARGUMENTS = dict(byte_width=4)

    def traces_of_interest(self):
        return [
            self.dut.source.payload,
            self.dut.source.valid,
            self.dut.source.ready,

            self.dut.sink.payload,
            self.dut.sink.valid,
            self.dut.sink.ready,
        ]

    @sync_test_case
    def test_basic(self):
        # yield from self.advance_cycles(2)

        self.assertEqual((yield self.dut.source.ready), 1)

        yield self.dut.source.payload.eq(0xCAFEBABE)
        yield self.dut.source.valid.eq(1)
        yield

        yield self.dut.source.valid.eq(0)
        yield

        self.assertEqual((yield self.dut.source.ready), 0)

        yield self.dut.source.payload.eq(0xDEADBEEF)
        yield self.dut.source.valid.eq(1)
        yield

        self.assertEqual((yield self.dut.sink.payload), 0xBE)
        self.assertEqual((yield self.dut.sink.valid),   1)

        yield self.dut.sink.ready.eq(1)
        yield
        yield

        self.assertEqual((yield self.dut.sink.payload), 0xBA)
        self.assertEqual((yield self.dut.sink.valid),   1)
        yield

        self.assertEqual((yield self.dut.sink.payload), 0xFE)
        self.assertEqual((yield self.dut.sink.valid),   1)
        yield

        self.assertEqual((yield self.dut.source.ready), 1)
        self.assertEqual((yield self.dut.sink.payload), 0xCA)
        self.assertEqual((yield self.dut.sink.valid),   1)        

        yield self.dut.source.valid.eq(0)
        yield

        self.assertEqual((yield self.dut.source.ready), 0)
        self.assertEqual((yield self.dut.sink.payload), 0xEF)
        self.assertEqual((yield self.dut.sink.valid),   1)
        yield

        self.assertEqual((yield self.dut.sink.payload), 0xBE)
        self.assertEqual((yield self.dut.sink.valid),   1)
        yield

        self.assertEqual((yield self.dut.sink.payload), 0xAD)
        self.assertEqual((yield self.dut.sink.valid),   1)
        yield

        self.assertEqual((yield self.dut.sink.payload), 0xDE)
        self.assertEqual((yield self.dut.sink.valid),   1)
        yield

        self.assertEqual((yield self.dut.source.ready), 1)
        self.assertEqual((yield self.dut.sink.valid),   0)
