from amaranth import *
from amaranth.lib import wiring

from hicart.debug.serial import FT245Streamer, FT245Reader
from hicart.interface.flash import FlashWishboneInterface
from hicart.utils.cli import main_runner


class Top(Elaboratable):

    def elaborate(self, platform):
        m = Module()

        m.submodules.car                                    = platform.clock_domain_generator()
        m.submodules.flash_io           = flash_io          = platform.flash_io()
        m.submodules.flash_interface    = flash_interface   = FlashWishboneInterface()

        wiring.connect(m, flash_interface.qspi_ce, flash_io.qspi_ce)

        address = Signal(24, reset=0x800000)
        counter = Signal(24)

        with m.FSM():

            with m.State("INITIAL"):
                m.next = "DELAY"
                m.d.sync += counter.eq(0)

            with m.State("DELAY"):
                m.d.sync += counter.eq(counter + 1)
                with m.If(counter == 10000000):
                    m.d.sync += counter.eq(0)
                    m.next = "IDLE"

            with m.State("IDLE"):
                m.next = "BEGIN"

            with m.State("BEGIN"):
                m.d.comb += flash_interface.bus.cyc  .eq(1)
                m.d.comb += flash_interface.bus.stb  .eq(1)

                with m.If(~flash_interface.bus.stall):
                    m.next = "RUNNING"

            with m.State("RUNNING"):
                m.d.comb += flash_interface.bus.cyc  .eq(1)

                with m.If(flash_interface.bus.ack):
                    m.next = "DELAY"

                    m.d.sync += [
                        address         .eq(address + 1)
                    ]

        m.d.comb += [
            flash_interface.bus.adr     .eq(address)
        ]



        m.submodules.streamer = streamer = FT245Streamer(byte_width=4)

        m.d.comb += [
            streamer.stream.payload     .eq(flash_interface.bus.dat_r),
            streamer.stream.valid       .eq(flash_interface.bus.ack)
        ]




        pmod = platform.request('pmod')

        m.d.comb += [
            pmod.d.o[0].eq(ClockSignal('sync')),
            pmod.d.o[1].eq(flash_io.qspi_ce.cs_n),
            pmod.d.o[2].eq(flash_io.spi_clk),

            pmod.d.o[3].eq(flash_io.qspi_ce.d.i[0]),
            pmod.d.o[4].eq(flash_io.qspi_ce.d.i[1]),
            pmod.d.o[5].eq(flash_io.qspi_ce.d.i[2]),
            pmod.d.o[6].eq(flash_io.qspi_ce.d.i[3]),
            pmod.d.o[7].eq(flash_io.qspi_ce.d.oe[0]),

            pmod.d.oe.eq(1),
        ]

        return m

if __name__ == "__main__":
    main_runner(Top(), do_program=True)
    FT245Reader(4).run()
