from amaranth import *
from amaranth.lib import wiring
import pyftdi.serialext

from hicart.interface.ft245 import FT245Interface
from hicart.soc.stream import ByteDownConverter
from hicart.utils.cli import main_runner


class Top(Elaboratable):

    def __init__(self):
        pass

    def elaborate(self, platform):
        m = Module()

        m.submodules.car           = platform.clock_domain_generator()
        m.submodules.iface = iface = FT245Interface()
        m.submodules.dc    = dc    = ByteDownConverter(byte_width=4)

        usb_fifo = platform.request('usb_fifo')
        pmod     = platform.request('pmod')

        wiring.connect(m, iface.bus, usb_fifo)

        m.d.comb += [
            dc.source.payload   .eq(0xCAFEBABE),
            dc.source.valid     .eq(dc.source.ready),
            dc.sink             .connect(iface.tx),
        ]

        m.d.comb += [
            pmod.d.o[0]         .eq(iface.tx.ready),
            pmod.d.o[1]         .eq(usb_fifo.d.oe),
            pmod.d.o[2]         .eq(usb_fifo.rxf.i),
            pmod.d.o[3]         .eq(usb_fifo.txe.i),
            pmod.d.o[4]         .eq(usb_fifo.rd.o),
            pmod.d.o[5]         .eq(usb_fifo.wr.o),
            pmod.d.o[6]         .eq(ClockSignal()),
            pmod.d.o[7]         .eq(ResetSignal()),
            pmod.d.oe           .eq(1),
        ]

        return m


def read_serial():
    port = pyftdi.serialext.serial_for_url('ftdi://ftdi:2232h:FT5RTNBA/1', baudrate=3000000)
    port.reset_input_buffer()

    while True:
        b = port.read()
        print(b)

if __name__ == "__main__":
    main_runner(Top(), do_program=True)
    read_serial()
