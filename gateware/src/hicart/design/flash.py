from amaranth import *
from amaranth.lib import wiring

from hicart.debug.serial import FT245Streamer, FT245Reader
from hicart.controller.flash import WishboneFlashController
from hicart.utils.cli import main_runner


class Top(Elaboratable):

    def elaborate(self, platform):
        m = Module()

        m.submodules.car                        = platform.clock_domain_generator()
        m.submodules.flash_io   = flash_io      = platform.flash_io()
        m.submodules.flash_ctrl = flash_ctrl    = WishboneFlashController(data_width=16)

        wiring.connect(m, flash_ctrl.bus, flash_io.bus)

        address = Signal(24, init=0x400000)
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
                m.d.comb += flash_ctrl.wb.cyc  .eq(1)
                m.d.comb += flash_ctrl.wb.stb  .eq(1)

                with m.If(~flash_ctrl.wb.stall):
                    m.next = "RUNNING"

            with m.State("RUNNING"):
                m.d.comb += flash_ctrl.wb.cyc  .eq(1)

                with m.If(flash_ctrl.wb.ack):
                    m.next = "DELAY"

                    m.d.sync += [
                        address         .eq(address + 1)
                    ]

        m.d.comb += [
            flash_ctrl.wb.adr     .eq(address)
        ]

        m.submodules.streamer = streamer = FT245Streamer(byte_width=2)

        m.d.comb += [
            streamer.stream.payload     .eq(flash_ctrl.wb.dat_r),
            streamer.stream.valid       .eq(flash_ctrl.wb.ack)
        ]

        pmod = platform.request("pmod")

        m.d.comb += [
            pmod.d.o[0].eq(ClockSignal("sync")),
            pmod.d.o[1].eq(flash_io.bus.cs_n),
            pmod.d.o[2].eq(flash_io.sck),

            pmod.d.o[3].eq(flash_io.bus.d.i[0]),
            pmod.d.o[4].eq(flash_io.bus.d.i[1]),
            pmod.d.o[5].eq(flash_io.bus.d.i[2]),
            pmod.d.o[6].eq(flash_io.bus.d.i[3]),
            pmod.d.o[7].eq(flash_io.bus.d.oe[0]),

            pmod.d.oe.eq(1),
        ]

        return m

if __name__ == "__main__":
    main_runner(Top(), do_program=True)
    FT245Reader(byte_width=2).run()
