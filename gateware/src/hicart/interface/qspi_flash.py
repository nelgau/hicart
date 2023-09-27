from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth_soc import wishbone
from amaranth_soc.memory import MemoryMap

from hicart.utils.plat import TristateSignature


class QSPISignature(wiring.Signature):
    def __init__(self):
        super().__init__({
            # The sck signal enables a gated, inverted clock output in the Home Invader platform,
            # which is otherwise held high. When cs_n goes low, this output is driven onto the
            # physical sck qspi pin using the ECP5's USRMCLK primitive.
            "sck":  Out(1),
            "cs_n": Out(1),
            "d":    Out(TristateSignature(4)),
        })


class QSPIFlashInterface(wiring.Component):

    # You can change the data width of the interface by adjusting the lines marked with "data width"

    qspi:       Out(QSPISignature())

    start:      In(1)
    address:    In(24)
    idle:       Out(1)
    valid:      Out(1)
    data:       Out(8)                                                  # Data width

    def __init__(self):
        super().__init__()

        self._in_shift  = Signal(32)
        self._out_shift = Signal(32)
        self._counter   = Signal(3)

    def elaborate(self, platform):
        m = Module()

        cs = Signal()

        m.d.sync += [
            self._in_shift[4:]      .eq(self._in_shift[:4]),            # Data width (see _out_shift)
            self._out_shift[4:]     .eq(self._out_shift[:28]),
            self._in_shift[0:4]     .eq(self.qspi.d.i),
            self._out_shift[0:4]    .eq(0),

            self.valid              .eq(0),
        ]

        m.d.comb += [
            self.qspi.d.o           .eq(self._out_shift[28:32]),
            self.data               .eq(self._in_shift),

            self.qspi.cs_n          .eq(~cs),
            self.idle               .eq(0),
        ]

        with m.If(self._counter > 0):
            m.d.sync += [
                self._counter       .eq(self._counter - 1)
            ]

        current_address     = Signal(24)

        with m.FSM():

            with m.State("INITIAL"):
                m.next = "STARTUP"
                m.d.sync += self._counter       .eq(7)

            with m.State("STARTUP"):
                with m.If(self._counter == 0):
                    m.next = "IDLE"

            with m.State("IDLE"):
                m.d.comb += self.idle           .eq(1)

                with m.If(self.start):
                    m.next = "START"
                    m.d.sync += [
                        current_address         .eq(self.address),
                    ]

            with m.State("START"):
                m.next = "COMMAND"                    
                m.d.sync += [
                    self._counter               .eq(7),
                    self._out_shift             .eq(0x11101011),
                    self.qspi.d.oe              .eq(0x1),

                    cs                          .eq(1),
                    self.qspi.sck               .eq(1),
                ]

            with m.State("COMMAND"):
                with m.If(self._counter == 0):
                    m.next = "ADDRESS"
                    m.d.sync += [                 
                        self._counter           .eq(7),
                        self._out_shift[8:32]   .eq(current_address),
                        self._out_shift[0:8]    .eq(0xF0),
                        self.qspi.d.oe          .eq(0xF),
                    ]

            with m.State("ADDRESS"):
                with m.If(self._counter == 0):
                    m.next = "DUMMY"
                    m.d.sync += [
                        self._counter           .eq(3), 
                        self.qspi.d.oe          .eq(0x0),
                    ]

            with m.State("DUMMY"):
                with m.If(self._counter == 0):
                    m.next = "DATA"
                    m.d.sync += [
                        self._counter           .eq(1),                 # Data width
                    ]   

            with m.State("DATA"):
                with m.If(self._counter == 0):
                    m.next = "WAITING"
                    m.d.sync += [                        
                        self.valid              .eq(1),
                        self.qspi.sck           .eq(0),
                    ]

            with m.State("WAITING"):
                m.d.comb += self.idle           .eq(1)

                with m.If(self.start):
                    m.d.sync += [
                        current_address         .eq(self.address),
                    ]                    

                    with m.If(self.address == current_address + 1):
                        m.next = "DATA"
                        m.d.sync += [
                            self._counter       .eq(1),                 # Data width
                            self.qspi.sck       .eq(1),
                        ]
                    with m.Else():
                        m.next = "RECOVERY"
                        m.d.sync += [
                            self._counter       .eq(7),
                            cs                  .eq(0),
                        ]

            with m.State("RECOVERY"):
                with m.If(self._counter == 0):
                    m.next = "START"

        return m


class QSPIFlashWishboneInterface(wiring.Component):
    qspi:       Out(QSPISignature())
    bus:        In(wishbone.Signature(addr_width=24, data_width=8, features={"stall"}))

    def __init__(self):
        super().__init__()

        memory_map = MemoryMap(addr_width=24, data_width=8)
        memory_map.add_resource(self, size=2**24, name='qspi_flash')
        self.bus.memory_map = memory_map

    def elaborate(self, platform):
        m = Module()

        m.submodules.interface = interface = QSPIFlashInterface()

        wiring.connect(m, interface.qspi, wiring.flipped(self.qspi))

        m.d.comb += [
            interface.start         .eq(self.bus.cyc & self.bus.stb),
            interface.address       .eq(self.bus.adr),

            self.bus.stall          .eq(~interface.idle),
            self.bus.dat_r          .eq(interface.data),
            self.bus.ack            .eq(interface.valid),
        ]

        return m
