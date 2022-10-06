from amaranth import *
from amaranth.sim import *

from hicart.interface.ft245 import  FT245Interface
from hicart.test.pysim.utils import ModuleTestCase, sync_test_case


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
