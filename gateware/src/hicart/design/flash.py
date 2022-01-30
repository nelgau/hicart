from amaranth import *

from hicart.debug.serial import FT245Streamer, FT245Reader
from hicart.interface.qspi_flash import QSPIFlashWishboneInterface
from hicart.utils.cli import main_runner


class Top(Elaboratable):

    def elaborate(self, platform):
        m = Module()

        m.submodules.car                               = platform.clock_domain_generator()
        m.submodules.flash_connector = flash_connector = platform.flash_connector()

        m.submodules.flash_interface = flash_interface = QSPIFlashWishboneInterface()

        m.d.comb += [
            flash_interface.bus     .connect(flash_connector.qspi),
        ]

        address = Signal(24)
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
                m.d.comb += flash_interface.wb.cyc  .eq(1)
                m.d.comb += flash_interface.wb.stb  .eq(1)

                with m.If(~flash_interface.wb.stall):
                    m.next = "RUNNING"

            with m.State("RUNNING"):
                m.d.comb += flash_interface.wb.cyc  .eq(1)

                with m.If(flash_interface.wb.ack):
                    m.next = "DELAY"

                    m.d.sync += [
                        address     .eq(address + 4)
                    ]

        m.d.comb += [
            flash_interface.wb.adr      .eq(address)
        ]



        m.submodules.streamer = streamer = FT245Streamer(byte_width=4)

        m.d.comb += [
            streamer.stream.payload     .eq(flash_interface.wb.dat_r),
            streamer.stream.valid       .eq(flash_interface.wb.ack)
        ]




        pmod = platform.request('pmod')

        m.d.comb += [
            pmod.d.o[0].eq(ClockSignal('sync')),
            pmod.d.o[1].eq(flash_connector.qspi.cs_n),
            pmod.d.o[2].eq(flash_connector.spi_clk),

            pmod.d.o[3].eq(flash_connector.qspi.d.i[0]),
            pmod.d.o[4].eq(flash_connector.qspi.d.i[1]),
            pmod.d.o[5].eq(flash_connector.qspi.d.i[2]),
            pmod.d.o[6].eq(flash_connector.qspi.d.i[3]),
            pmod.d.o[7].eq(flash_connector.qspi.d.oe[0]),

            pmod.d.oe.eq(1),
        ]        

        return m

if __name__ == "__main__":
    main_runner(Top())
    FT245Reader(4).run()
