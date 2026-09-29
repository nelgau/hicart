from amaranth import *
import pyftdi.serialext

from hicart.debug.serial import FT245Streamer
from hicart.utils.cli import main_runner


class Top(Elaboratable):

    def elaborate(self, platform):
        m = Module()

        cdg = platform.clock_domain_generator()
        streamer = FT245Streamer(byte_width=2)

        m.submodules.cdg = cdg
        m.submodules.streamer = streamer

        delay_counter = Signal(24)
        data_counter = Signal(2)

        with m.If(delay_counter != 0):
            m.d.sync += delay_counter.eq(delay_counter - 1)

        with m.If(delay_counter == 0):
            with m.If(~streamer.stream.valid):
                m.d.sync += data_counter.eq(data_counter + 1)
                m.d.sync += streamer.stream.valid.eq(1)

                with m.Switch(data_counter):
                    with m.Case(0):
                        m.d.sync += streamer.stream.payload.eq(0x8037)
                    with m.Case(1):
                        m.d.sync += streamer.stream.payload.eq(0x1240)
                    with m.Case(2):
                        m.d.sync += streamer.stream.payload.eq(0x0000)
                    with m.Case(3):
                        m.d.sync += streamer.stream.payload.eq(0x000f)

        with m.If(streamer.stream.ready & streamer.stream.valid):
            m.d.sync += delay_counter.eq(10000000)
            m.d.sync += streamer.stream.valid.eq(0)

        return m


def read_serial():
    port = pyftdi.serialext.serial_for_url("ftdi://ftdi:2232h:FT5RTNBA/1", baudrate=3000000)
    port.reset_input_buffer()

    while True:
        data = port.read(size=2)
        value = int.from_bytes(data, byteorder="little")
        print(f"0x{value:04x}")

if __name__ == "__main__":
    main_runner(Top(), do_program=True)
    read_serial()
