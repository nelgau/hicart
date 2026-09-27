from amaranth import *
from amaranth.lib import wiring
import pyftdi.serialext

from hicart.controller.ft245 import FT245Controller
from hicart.soc.stream import ByteDownConverter
from hicart.utils.cli import main_runner


class Top(Elaboratable):

    def __init__(self):
        pass

    def elaborate(self, platform):
        m = Module()

        m.submodules.car                    = platform.clock_domain_generator()
        m.submodules.ft245_io   = ft245_io  = platform.ft245_io()
        m.submodules.iface      = iface     = FT245Controller()
        m.submodules.dc         = dc        = ByteDownConverter(byte_width=4)

        pmod     = platform.request("pmod")

        wiring.connect(m, iface.bus, ft245_io.bus)
        wiring.connect(m, iface.tx, dc.sink)

        m.d.comb += [
            dc.source.payload   .eq(0x12345678),
            dc.source.valid     .eq(dc.source.ready),
        ]

        m.d.comb += [
            pmod.d.o[0]         .eq(iface.tx.ready),
            pmod.d.o[1]         .eq(iface.bus.d.oe),
            pmod.d.o[2]         .eq(iface.bus.rxf),
            pmod.d.o[3]         .eq(iface.bus.txe),
            pmod.d.o[4]         .eq(iface.bus.rd),
            pmod.d.o[5]         .eq(iface.bus.wr),
            pmod.d.o[6]         .eq(ClockSignal()),
            pmod.d.o[7]         .eq(ResetSignal()),
            pmod.d.oe           .eq(1),
        ]

        return m


def read_serial():
    port = pyftdi.serialext.serial_for_url("ftdi://ftdi:2232h:FT5RTNBA/1", baudrate=3000000)
    port.reset_input_buffer()

    while True:
        b = port.read()
        print(f"0x{b[0]:02x}")

if __name__ == "__main__":
    main_runner(Top(), do_program=True)
    read_serial()
