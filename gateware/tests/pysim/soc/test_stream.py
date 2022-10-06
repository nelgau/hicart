from amaranth import *
from amaranth.sim import *

from hicart.soc.stream import ByteDownConverter
from hicart.test.utils import ModuleTestCase, sync_test_case


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
