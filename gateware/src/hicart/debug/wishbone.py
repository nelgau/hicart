import struct

from amaranth import *
from amaranth.sim import *
from amaranth_soc import wishbone

from hicart.interface.ft245 import FT245Interface
from hicart.soc.stream import BasicStream

from hicart.test.testcase import MultiProcessTestCase
from hicart.test.driver.stream import StreamDriver
from hicart.test.emulator.wishbone import WishboneEmulator


class StreamWishboneCommander(Elaboratable):

    def __init__(self):
        self.bus = wishbone.Interface(addr_width=32, data_width=32, features={"stall"})

        self.source = BasicStream(8)
        self.sink = BasicStream(8)

    def elaborate(self, platform):
        m = Module()

        count = Signal(8, reset=0)      # FIXME: Size this more appropriately later!

        address = Signal(32)
        perform_write = Signal()

        read_data = Signal(32)
        write_data = Signal(32)

        m.d.comb += [
            self.source.ready       .eq(0),
            self.sink.payload       .eq(0),
            self.sink.valid         .eq(0),

            self.bus.adr            .eq(address),
            self.bus.we             .eq(perform_write),
            self.bus.dat_w          .eq(write_data),
        ]

        with m.FSM():

            with m.State("IDLE"):
                m.d.comb += self.source.ready.eq(1)

                with m.If(self.source.valid):

                    with m.If(self.source.payload == 0x10):
                        m.next = "ADDRESS"
                        m.d.sync += [
                            count           .eq(3),
                            perform_write   .eq(0),
                        ]
                    with m.Elif(self.source.payload == 0x11):
                        m.next = "ADDRESS"
                        m.d.sync += [
                            count           .eq(3),
                            perform_write   .eq(1),
                        ]
                    with m.Else():
                        # Invalid command
                        # FIXME: Do something else?
                        m.next = "IDLE"

            with m.State("ADDRESS"):
                m.d.comb += self.source.ready.eq(1)

                with m.If(self.source.valid):

                    m.d.sync += [
                        address[8:]      .eq(address[:-8]),
                        address[:8]      .eq(self.source.payload),
                    ]

                    with m.If(count > 0):
                        m.d.sync += count.eq(count - 1)
                    with m.Else():

                        with m.If(perform_write):
                            m.next = "WRITE_DATA"
                            m.d.sync += count.eq(3)
                        with m.Else():
                            m.next = "OP_BEGIN"

            with m.State("WRITE_DATA"):
                m.d.comb += self.source.ready.eq(1)

                with m.If(self.source.valid):

                    m.d.sync += [
                        write_data[8:]      .eq(write_data[:-8]),
                        write_data[:8]      .eq(self.source.payload),
                    ]

                    with m.If(count > 0):
                        m.d.sync += count.eq(count - 1)
                    with m.Else():
                        m.next = "OP_BEGIN"

            with m.State("OP_BEGIN"):
                m.d.comb += self.bus.cyc      .eq(1)
                m.d.comb += self.bus.stb      .eq(1)

                with m.If(~self.bus.stall):
                    m.next = "OP_WAIT"

            with m.State("OP_WAIT"):
                m.d.comb += self.bus.cyc      .eq(1)

                with m.If(self.bus.ack):

                    with m.If(perform_write):
                        m.next = "ACK"
                    with m.Else():
                        m.next = "READ_DATA"
                        m.d.sync += [
                            count           .eq(3),
                            read_data       .eq(self.bus.dat_r)
                        ]

            with m.State("READ_DATA"):                
                m.d.comb += [
                    self.sink.payload       .eq(read_data[-8:]),
                    self.sink.valid         .eq(1),
                ]

                with m.If(self.sink.ready):

                    m.d.sync += [
                        read_data[8:]     .eq(read_data[:-8]),
                        read_data[:8]     .eq(0),
                    ]                    

                    with m.If(count > 0):
                        m.d.sync += count.eq(count - 1)
                    with m.Else():
                        m.next = "ACK"

            with m.State("ACK"):
                m.d.comb += [
                    self.sink.payload       .eq(0xDD),
                    self.sink.valid         .eq(1),
                ]

                with m.If(self.sink.ready):
                    m.next = "IDLE"

        return m

    def ports(self):
        return [
            self.bus,
            self.source,
            self.sink
        ]


class FT245WishboneCommander(Elaboratable):

    def __init__(self, domain='sync'):
        self.domain = domain

        self.bus = wishbone.Interface(addr_width=32, data_width=32, features={"stall"})

    def elaborate(self, platform):
        m = Module()

        m.submodules.iface = iface = FT245Interface()
        m.submodules.comm  = comm  = StreamWishboneCommander()

        usb_fifo = platform.request('usb_fifo')

        m.d.comb += [
            iface.rx    .connect(comm.source),
            comm.sink   .connect(iface.tx),

            iface.bus   .connect(usb_fifo),
            comm.bus    .connect(self.bus),
        ]

        # Convert our sync domain to the domain requested by the user, if necessary.
        if self.domain != "sync":
            m = DomainRenamer({"sync": self.domain})(m)

        return m


class FT245WishboneRemote:

    def __init__(self):
        import pyftdi.serialext

        self._port = pyftdi.serialext.serial_for_url('ftdi://ftdi:2232h:FT5RTNBA/1', baudrate=3000000)
        self._port.reset_input_buffer()    

    def read(self, address):
        self._port.write(struct.pack('>B', 0x10))
        self._port.write(struct.pack('>L', address))
        # self._port.flush()

        data = struct.unpack('>L', self._port.read(4))[0]
        ack  = struct.unpack('>B', self._port.read(1))[0]

        if ack != 0xDD:
            print(f"Got bad response! 0x{ack:02X}")

        return data

    def write(self, address, data):
        self._port.write(struct.pack('>B', 0x11))
        self._port.write(struct.pack('>L', address))
        self._port.write(struct.pack('>L', data))
        # self._port.flush()

        ack  = struct.unpack('>B', self._port.read(1))[0]

        if ack != 0xDD:
            print(f"Got bad response! 0x{ack:02X}")     


class StreamWishboneCommanderTest(MultiProcessTestCase):

    def test_simple(self):
        dut = StreamWishboneCommander()

        bus_emulator = WishboneEmulator(dut.bus, initial=0xFEEDFACE, delay=1, max_outstanding=1)
        source_driver = StreamDriver(dut.source)
        sink_driver = StreamDriver(dut.sink)

        def bus_process():
            yield Passive()
            yield from bus_emulator.emulate()

        def source_process():
            yield from source_driver.begin()

            # Read command
            yield from source_driver.produce([0x10])
            yield from source_driver.produce([0xCA, 0xFE, 0xBA, 0xBE])

            for i in range(4):
                yield

            # Write command
            yield from source_driver.produce([0x11])
            yield from source_driver.produce([0xDE, 0xAD, 0xBE, 0xEF])
            yield from source_driver.produce([0x12, 0x34, 0x56, 0x78])

        def sink_process():
            yield from sink_driver.begin()

            # Read command
            yield from sink_driver.consume(4)
            yield from sink_driver.consume()

            # Write command
            yield from sink_driver.consume()

        with self.simulate(dut, traces=dut.ports()) as sim:
            sim.add_clock(1.0 / 100e6, domain='sync')
            sim.add_sync_process(bus_process)
            sim.add_sync_process(source_process)
            sim.add_sync_process(sink_process)
