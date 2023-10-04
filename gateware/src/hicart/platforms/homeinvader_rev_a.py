import os
import subprocess

from amaranth import *
from amaranth.build import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth.vendor import LatticeECP5Platform
from amaranth_boards.resources import *

from hicart.interface.qspi_flash import QSPISignature
from hicart.utils.plat import get_all_resources

from hicart.vendor.ecp5pll import ECP5PLL, ECP5PLLConfig


__all__ = ["HomeInvaderRevAPlatform"]


class HomeInvaderRevADomainGenerator(Elaboratable):

    def elaborate(self, platform):
        m = Module()

        configs = [
            ECP5PLLConfig("sync", freq=80),
            ECP5PLLConfig("cic",  freq=40),
        ]

        m.submodules.pll = ECP5PLL(configs)

        return m


class HomeInvaderRevAFlashConnector(wiring.Component):
    qspi:       In(QSPISignature())
    spi_clk:    Out(1)

    def elaborate(self, platform):
        m = Module()

        m.submodules += Instance("USRMCLK",
            # Gated clock signal
            i_USRMCLKI=self.spi_clk,
            # Active-low output enable (tristate)
            i_USRMCLKTS=self.qspi.cs_n
        )

        qspi_pins = platform.request("qspi_flash")
        sync_clk = ClockSignal()

        m.d.comb += [
            # FIXME: Does this clock gating mux actually belong here? Can it
            # be refactored out into the QSPIFlashInterface module?
            qspi_pins.cs_n          .eq(self.qspi.cs_n),
            self.spi_clk            .eq(Mux(self.qspi.sck, ~sync_clk, 1)),
        ]

        for i in range(4):
            dq_pin = qspi_pins[f"dq{i}"]
            m.d.comb += [
                self.qspi.d.i[i]    .eq(dq_pin.i),
                dq_pin.o            .eq(self.qspi.d.o[i]),
                dq_pin.oe           .eq(self.qspi.d.oe[i]),
            ]

        return m


class HomeInvaderRevAPlatform(LatticeECP5Platform):
    device      = "LFE5U-12F"
    package     = "BG256"
    speed       = "6"
    default_clk = "clk12"

    clock_domain_generator = HomeInvaderRevADomainGenerator
    flash_connector = HomeInvaderRevAFlashConnector
    
    resources = [
        Resource("clk12", 0, Pins("J16", dir="i"), 
            Clock(12e6), Attrs(IO_TYPE="LVCMOS33")),

        Resource("n64_cart", 0,
            Subsignal("pi",
                Subsignal("ad",     Pins("A2 A3 A4 A5 A8 A9 A10 A11 B12 B11 B10 B9 B6 B5 B4 B3", dir="io"),
                    Attrs(PULLMODE="DOWN")),

                Subsignal("ale_h",  PinsN("A7", dir="i"),  Attrs(PULLMODE="UP")),
                Subsignal("ale_l",  PinsN("A6", dir="i"),  Attrs(PULLMODE="UP")),
                Subsignal("read",   PinsN("B8", dir="i"),  Attrs(PULLMODE="UP")),
                Subsignal("write",  PinsN("B7", dir="i"),  Attrs(PULLMODE="UP")),
            ),
            Subsignal("si",
                Subsignal("dclk",   Pins("A13", dir="i")),
                Subsignal("data",   Pins("B14", dir="io"), Attrs(PULLMODE="NONE")),
            ),
            Subsignal("cic",
                Subsignal("dclk",   Pins("A12", dir="i")),
                Subsignal("data",   Pins("B13", dir="io"), Attrs(PULLMODE="NONE")),
            ),
            Subsignal("reset",      PinsN("A14", dir="i"), Attrs(PULLMODE="UP")),
            Subsignal("nmi",        PinsN("C13", dir="i"), Attrs(PULLMODE="UP")),
            
            Attrs(IO_TYPE="LVCMOS33", SLEWRATE="SLOW")
        ),

        Resource("usb_fifo", 0,
            Subsignal("d",        Pins("L15 M16 M15 N16 N14 P16 P15 R16", dir="io")),
            Subsignal("rxf",      Pins("R15", dir="i"), Attrs(PULLMODE="NONE")),
            Subsignal("txe",      Pins("T15", dir="i"), Attrs(PULLMODE="NONE")),
            Subsignal("rd",       Pins("R14", dir="o")),
            Subsignal("wr",       Pins("T14", dir="o")),
            Subsignal("siwu",     Pins("R13", dir="o")),

            # Only used in synchronous mode.
            Subsignal("clkout",   Pins("L16", dir="i")),
            Subsignal("oe",       Pins("T13", dir="o"))
        ),

        Resource("qspi_flash", 0,
            # Subsignal("sck",       Pins("R14", dir="o")),
            Subsignal("cs_n",       Pins("N8", dir="o"), Attrs(PULLMODE="UP")),
            Subsignal("dq0",        Pins("T8", dir="io")),
            Subsignal("dq1",        Pins("T7", dir="io")),
            Subsignal("dq2",        Pins("M7", dir="io")),
            Subsignal("dq3",        Pins("N7", dir="io")),
        ),

        Resource("ram", 0,
            Subsignal("clk",        DiffPairs("J1", "J2", dir="o"), Attrs(IO_TYPE="LVCMOS18D")),
            Subsignal("dq",         Pins("C1 F2 B2 C3 B1 D3 E1 F3", dir="io")),
            Subsignal("rwds",       Pins("D1", dir="io")),
            Subsignal("cs",         PinsN("K1", dir="o")),
            Subsignal("reset",      PinsN("K2", dir="o")),

            Attrs(IO_TYPE="LVCMOS18", SLEWRATE="FAST")
        ),

        Resource("pmod", 0,
            Subsignal("d",        Pins("C4 C5 C6 C7 D4 D5 D6 D7", dir="io"))
        ),

        *LEDResources(pins="C16 B16 C15 B15 E15 C14 D14 E14",
            attrs=Attrs(IO_TYPE="LVCMOS33")),
    ]

    connectors = [
        Connector("pmod", 0, "C4 C5 C6 C7 - - D4 D5 D6 D7 - -")
    ]

    def get_leds(self):
        return Cat([l.o for l in get_all_resources(self, 'led')])

    @property
    def required_tools(self):
        return super().required_tools + [
          "ecpprog"
        ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = {
            "ecppack_opts": "--compress --freq 38.8"
        }
        return super().toolchain_prepare(fragment, name, **overrides, **kwargs)

    def toolchain_program(self, products, name, **kwargs):
        ecpprog = os.environ.get("ECPPROG", "ecpprog")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call([ecpprog, "-d", "s:0x0403:0x6010:FT5YLSVU", "-I", "B", "-S", bitstream_filename])

if __name__ == "__main__":
    from amaranth_boards.test.blinky import *
    HomeInvaderRevAPlatform().build(Blinky(), do_program=True)
