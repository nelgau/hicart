from amaranth import *
import pyftdi.serialext

from hicart.interface.ft245 import FT245Interface
from hicart.soc.stream import ByteDownConverter
from hicart.utils.cli import main_runner


class Top(Elaboratable):

    def __init__(self):
        pass

    def elaborate(self, platform):
        m = Module()

        usb_fifo = platform.request('usb_fifo')
        pmod     = platform.request('pmod')

        m.submodules.car           = platform.clock_domain_generator()
        m.submodules.iface = iface = FT245Interface()
        m.submodules.dc    = dc    = ByteDownConverter(byte_width=4)

        m.d.comb += [
            dc.source.payload   .eq(0xCAFEBABE),
            dc.source.valid     .eq(dc.source.ready),

            dc.sink             .connect(iface.tx),
        ]

        m.d.comb += [
            iface.bus.d.i       .eq(usb_fifo.d.i),
            usb_fifo.d.o        .eq(iface.bus.d.o),
            usb_fifo.d.oe       .eq(iface.bus.d.oe),
            
            iface.bus.rxf       .eq(usb_fifo.rxf),
            iface.bus.txe       .eq(usb_fifo.txe),
            usb_fifo.rd         .eq(iface.bus.rd),
            usb_fifo.wr         .eq(iface.bus.wr),
        ]

        # m.d.comb += [
        #     usb_fifo.rd         .eq(1),
        #     usb_fifo.wr         .eq(1),
        # ]

        m.d.comb += [
            pmod.d.o[0]         .eq(iface.tx.ready),
            pmod.d.o[1]         .eq(usb_fifo.d.oe),            
            pmod.d.o[2]         .eq(usb_fifo.rxf),
            pmod.d.o[3]         .eq(usb_fifo.txe),
            pmod.d.o[4]         .eq(usb_fifo.rd),
            pmod.d.o[5]         .eq(usb_fifo.wr),
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
    main_runner(Top())
    read_serial()
