from amaranth import *
from amaranth.sim import *

from hicart.interface.qspi_flash import QSPIFlashInterface, QSPIFlashWishboneInterface
from hicart.test.utils import ModuleTestCase, sync_test_case


class QSPIFlashInterfaceTest(ModuleTestCase):
    FRAGMENT_UNDER_TEST = QSPIFlashInterface

    def traces_of_interest(self):
        return [
            self.dut.qspi.sck,
            self.dut.qspi.cs_n,
            self.dut.qspi.d.i,
            self.dut.qspi.d.o,
            self.dut.qspi.d.oe,

            self.dut.start,
            self.dut.address,
            self.dut.idle,
            self.dut.valid,
            self.dut.data,

            self.dut._in_shift,
            self.dut._out_shift,
            self.dut._counter,
        ]    

    @sync_test_case
    def test_basic(self):
        yield from self.advance_cycles(10)

        #

        yield self.dut.address.eq(0x876543)
        yield self.dut.start.eq(1)
        yield
        yield self.dut.start.eq(0)
        yield

        yield from self.advance_cycles(20)

        for x in [0xF, 0xE, 0xD, 0xC, 0xB, 0xA, 0x9, 0x8]:
            yield self.dut.qspi.d.i.eq(x)
            yield

        yield self.dut.qspi.d.i.eq(0)
        yield

        yield from self.advance_cycles(5)

        #

        yield self.dut.address.eq(0x876544)
        yield self.dut.start.eq(1)
        yield
        yield self.dut.start.eq(0)        

        for x in [0x7, 0x6, 0x5, 0x4, 0x3, 0x2, 0x1, 0x0]:
            yield self.dut.qspi.d.i.eq(x)
            yield

        yield self.dut.qspi.d.i.eq(0)
        yield

        yield from self.advance_cycles(5)

        #

        yield self.dut.address.eq(0x876546)
        yield self.dut.start.eq(1)
        yield
        yield self.dut.start.eq(0)
        yield

        yield from self.advance_cycles(28)

        for x in [0xC, 0xA, 0xF, 0xE, 0xB, 0xA, 0xB, 0xE]:
            yield self.dut.qspi.d.i.eq(x)
            yield

        yield self.dut.qspi.d.i.eq(0)
        yield

        yield from self.advance_cycles(20) 


class QSPIFlashWishboneInterfaceTest(ModuleTestCase):
    FRAGMENT_UNDER_TEST = QSPIFlashWishboneInterface

    def traces_of_interest(self):
        return [
            self.dut.qspi.sck,
            self.dut.qspi.cs_n,
            self.dut.qspi.d.i,
            self.dut.qspi.d.o,
            self.dut.qspi.d.oe,

            self.dut.bus.cyc,
            self.dut.bus.stb,
            self.dut.bus.stall,
            self.dut.bus.ack,
            self.dut.bus.adr,
            self.dut.bus.dat_r
        ]

    @sync_test_case
    def test_basic(self):
        yield from self.advance_cycles(10)

        #

        yield self.dut.bus.adr.eq(0x876543)
        yield self.dut.bus.cyc.eq(1)
        yield self.dut.bus.stb.eq(1)
        yield
        yield self.dut.bus.stb.eq(0)
        yield

        yield from self.advance_cycles(20)

        for x in [0xF, 0xE, 0xD, 0xC, 0xB, 0xA, 0x9, 0x8]:
            yield self.dut.qspi.d.i.eq(x)
            yield

        yield self.dut.qspi.d.i.eq(0)
        yield        

        yield self.dut.bus.cyc.eq(0)
        yield

        yield from self.advance_cycles(5)


        #

        yield self.dut.bus.adr.eq(0x876544)
        yield self.dut.bus.cyc.eq(1)
        yield self.dut.bus.stb.eq(1)
        yield
        yield self.dut.bus.stb.eq(0)   

        for x in [0x7, 0x6, 0x5, 0x4, 0x3, 0x2, 0x1, 0x0]:
            yield self.dut.qspi.d.i.eq(x)
            yield

        yield self.dut.qspi.d.i.eq(0)
        yield

        yield self.dut.bus.cyc.eq(0)
        yield

        yield from self.advance_cycles(5)

        #

        yield self.dut.bus.adr.eq(0x876546)
        yield self.dut.bus.cyc.eq(1)
        yield self.dut.bus.stb.eq(1)
        yield
        yield self.dut.bus.stb.eq(0)
        yield

        yield from self.advance_cycles(28)

        for x in [0xC, 0xA, 0xF, 0xE, 0xB, 0xA, 0xB, 0xE]:
            yield self.dut.qspi.d.i.eq(x)
            yield

        yield self.dut.qspi.d.i.eq(0)
        yield

        yield self.dut.bus.cyc.eq(0)
        yield

        yield from self.advance_cycles(20)
