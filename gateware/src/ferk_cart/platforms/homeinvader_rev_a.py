import os
import subprocess

from amaranth import *
from amaranth.build import *
from amaranth.hdl.ast import Fell
from amaranth.vendor.lattice_ecp5 import *
from amaranth_boards.resources import *

from ferk_cart.interface.qspi_flash import QSPIBus
from ferk_cart.utils.plat import get_all_resources

__all__ = ["HomeInvaderRevAPlatform"]

class HomeInvaderRevADomainGenerator(Elaboratable):
    """ Clock generator for Rev A boards. """

    def elaborate(self, platform):
        m = Module()

        # Grab our default input clock.
        input_clock = platform.request(platform.default_clk, dir="i")        

        # Create our domains; but don't do anything else for them, for now.
        m.domains.sync = ClockDomain()
        m.domains.cic  = ClockDomain()
        m.domains.slow = ClockDomain()

        locked = Signal()
        clk80  = Signal()
        clk40  = Signal()
        clk20  = Signal()


        # 60 Mhz sync clock
        # ref_div  = 1
        # fb_div   = 5
        # clk0_div = 10
        # clk1_div = 15
        # clk2_div = 30
        # clk0_freq = "60"
        # clk1_freq = "40"
        # clk2_freq = "20"

        # 80 Mhz sync clock
        ref_div  = 3
        fb_div   = 20
        clk0_div = 7
        clk1_div = 14
        clk2_div = 28
        clk0_freq = "80"
        clk1_freq = "40"
        clk2_freq = "20"        



        m.submodules.pll = Instance("EHXPLLL",
                # Clock in
                i_CLKI=input_clock,

                # Generated clock outputs.
                o_CLKOP=clk80,
                o_CLKOS=clk40,
                o_CLKOS2=clk20,

                # Status
                o_LOCK=locked,

                # PLL parameters
                p_PLLRST_ENA="DISABLED",
                p_INTFB_WAKE="DISABLED",
                p_STDBY_ENABLE="DISABLED",
                p_DPHASE_SOURCE="DISABLED",
                p_OUTDIVIDER_MUXA="DIVA",
                p_OUTDIVIDER_MUXB="DIVB",
                p_OUTDIVIDER_MUXC="DIVC",
                p_OUTDIVIDER_MUXD="DIVD",
                p_CLKI_DIV = ref_div,                     # Was 3           
                p_CLKOP_ENABLE = "ENABLED",
                p_CLKOP_DIV = clk0_div,                   # Was 7
                p_CLKOP_CPHASE = 3,
                p_CLKOP_FPHASE = 0,
                p_CLKOS_ENABLE = "ENABLED",
                p_CLKOS_DIV = clk1_div,
                p_CLKOS_CPHASE = 3,
                p_CLKOS_FPHASE = 0,
                p_CLKOS2_ENABLE = "ENABLED",
                p_CLKOS2_DIV = clk2_div,
                p_CLKOS2_CPHASE = 3,
                p_CLKOS2_FPHASE = 0,                
                p_FEEDBK_PATH = "CLKOP",
                p_CLKFB_DIV = fb_div,                   # Was 20

                # Internal feedback
                i_CLKFB=clk80,

                # Control signals
                i_RST=0,
                i_STDBY=0,
                i_PHASESEL0=0,
                i_PHASESEL1=0,
                i_PHASEDIR=1,
                i_PHASESTEP=1,
                i_PHASELOADREG=1,
                i_PLLWAKESYNC=0,

                # Output Enables.
                i_ENCLKOP=0,                

                # Synthesis attributes.
                a_FREQUENCY_PIN_CLKI="12",
                a_FREQUENCY_PIN_CLKOP=clk0_freq,         # Was 80
                a_FREQUENCY_PIN_CLKOS=clk1_freq,
                a_FREQUENCY_PIN_CLKOS2=clk2_freq,
                a_ICP_CURRENT="12",
                a_LPF_RESISTOR="8",
                a_MFG_ENABLE_FILTEROPAMP="1",
                a_MFG_GMCREF_SEL="2"
        )

        m.d.comb += [
            ClockSignal("sync")    .eq(clk80),
            ClockSignal("cic")     .eq(clk40),
            ClockSignal("slow")    .eq(clk20),

            ResetSignal("sync")    .eq(~locked),
            ResetSignal("cic")     .eq(~locked),
            ResetSignal("slow")    .eq(~locked),
        ]

        return m


class HomeInvaderRevAFlashConnector(Elaboratable):

    def __init__(self):
        self.qspi = QSPIBus()
        self.spi_clk = Signal()

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
            Subsignal("ad",       Pins("A2 A3 A4 A5 A8 A9 A10 A11 B12 B11 B10 B9 B6 B5 B4 B3", dir="io"),
                Attrs(PULLMODE="DOWN")),

            Subsignal("ale_h",    PinsN("A7", dir="i"),  Attrs(PULLMODE="UP")),
            Subsignal("ale_l",    PinsN("A6", dir="i"),  Attrs(PULLMODE="UP")),
            Subsignal("read",     PinsN("B8", dir="i"),  Attrs(PULLMODE="UP")),
            Subsignal("write",    PinsN("B7", dir="i"),  Attrs(PULLMODE="UP")),

            Subsignal("s_clk",    Pins("A13", dir="i")),
            Subsignal("s_data",   Pins("B14", dir="io"), Attrs(PULLMODE="NONE")),

            Subsignal("cic_dclk", Pins("A12", dir="i")),
            Subsignal("cic_data", Pins("B13", dir="io"), Attrs(PULLMODE="NONE")),

            Subsignal("reset",    PinsN("A14", dir="i"), Attrs(PULLMODE="UP")),
            Subsignal("nmi",      PinsN("C13", dir="i"), Attrs(PULLMODE="UP")),

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
