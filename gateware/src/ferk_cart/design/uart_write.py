import time

from amaranth import *
import pyftdi.serialext

from ferk_cart.interface.ft245 import FT245Interface
from ferk_cart.utils.cli import main_runner


class Top(Elaboratable):

    def elaborate(self, platform):
        m = Module()

        usb_fifo = platform.request('usb_fifo')
        leds = platform.get_leds()

        m.submodules.car           = platform.clock_domain_generator()
        m.submodules.iface = iface = FT245Interface()

        data_in = Signal(8)

        m.d.comb += iface.rx.ready.eq(1)

        with m.If(iface.rx.valid):
            m.d.sync += data_in.eq(iface.rx.payload)

        m.d.comb += [
            iface.bus       .connect(usb_fifo),

            leds.eq(data_in)
        ]

        return m


def write_serial():
    port = pyftdi.serialext.serial_for_url('ftdi://ftdi:2232h:FT5RTNBA/1', baudrate=3000000)
    port.reset_input_buffer()

    def do_write(string):
        port.write(string.encode('utf-8'))

    while True:
        do_write('3')
        time.sleep(0.25)
        do_write('x')
        time.sleep(0.25)

if __name__ == "__main__":
    main_runner(Top())
    write_serial()
