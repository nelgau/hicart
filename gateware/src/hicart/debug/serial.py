from amaranth import *
from amaranth.lib import wiring

from hicart.controller.ft245 import FT245Controller
from hicart.soc.stream import BasicStream, ByteDownConverter


class FT245Streamer(Elaboratable):

    def __init__(self, byte_width, domain="sync"):
        self.byte_width = byte_width
        self.domain = domain

        self.stream = BasicStream(width=8 * byte_width)

    def elaborate(self, platform):
        m = Module()

        m.submodules.ft245_io   = ft245_io  = platform.ft245_io()
        m.submodules.iface      = iface     = FT245Controller()
        m.submodules.dc         = dc        = ByteDownConverter(byte_width=self.byte_width)

        wiring.connect(m, iface.bus, ft245_io.bus)

        m.d.comb += [
            self.stream     .connect(dc.source),
            dc.sink         .connect(iface.tx),
        ]

        # Convert our sync domain to the domain requested by the user, if necessary.
        if self.domain != "sync":
            m = DomainRenamer({"sync": self.domain})(m)

        return m


class FT245Reader():

    def __init__(self, byte_width):
        self.byte_width = byte_width

        import pyftdi.serialext

        self._port = pyftdi.serialext.serial_for_url("ftdi://ftdi:2232h:FT5RTNBA/1", baudrate=3000000)
        self._port.reset_input_buffer()

    def run(self):
        print("Listening for serial data...")
        while True:
            payload = self._port.read(self.byte_width)
            print(bytes(reversed(payload)).hex(' '))
