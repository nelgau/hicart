import time

from amaranth import *
from amaranth.lib import wiring
import pyftdi.serialext

from hicart.interface.ft245 import FT245Interface
from hicart.utils.cli import main_runner


class Top(Elaboratable):

    def elaborate(self, platform):
        m = Module()

        m.submodules.car           = platform.clock_domain_generator()
        m.submodules.iface = iface = FT245Interface()

        usb_fifo = platform.request('usb_fifo')
        leds = platform.get_leds()

        wiring.connect(m, iface.bus, usb_fifo)

        data_in = Signal(8)

        m.d.comb += iface.rx.ready.eq(1)

        with m.If(iface.rx.valid):
            m.d.sync += data_in.eq(iface.rx.payload)

        m.d.comb += [
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
    main_runner(Top(), do_program=True)
    write_serial()
