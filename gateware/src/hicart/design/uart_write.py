import time

from amaranth import *
from amaranth.lib import wiring
import pyftdi.serialext

from hicart.controller.ft245 import FT245Controller
from hicart.utils.cli import main_runner


class Top(Elaboratable):

    def elaborate(self, platform):
        m = Module()

        leds = platform.request("leds")

        m.submodules.car                    = platform.clock_domain_generator()
        m.submodules.ft245_io   = ft245_io  = platform.ft245_io()
        m.submodules.iface      = iface     = FT245Controller()

        wiring.connect(m, iface.bus, ft245_io.bus)

        data_in = Signal(8)

        m.d.comb += iface.rx.ready.eq(1)
        m.d.comb += leds.d.o.eq(data_in)

        with m.If(iface.rx.valid):
            m.d.sync += data_in.eq(iface.rx.payload)

        return m


def write_serial():
    port = pyftdi.serialext.serial_for_url("ftdi://ftdi:2232h:FT5RTNBA/1", baudrate=3000000)
    port.reset_input_buffer()

    def do_write(string):
        port.write(string.encode("utf-8"))

    while True:
        do_write("3")
        time.sleep(0.25)
        do_write("x")
        time.sleep(0.25)

if __name__ == "__main__":
    main_runner(Top(), do_program=True)
    write_serial()
