import os
import subprocess

from amaranth import *
from amaranth.build import *
from amaranth.lib import cdc, wiring
from amaranth.lib.wiring import In, Out
from amaranth.vendor import LatticeECP5Platform

from hicart.controller import flash, ft245
from hicart.n64.cart import *

from hicart.vendor.ecp5pll import ECP5PLL, ECP5PLLConfig


__all__ = ["HomeInvaderRevAPlatform"]


class HomeInvaderRevADomainGenerator(Elaboratable):

    def elaborate(self, platform):
        m = Module()

        configs = [
            ECP5PLLConfig("sync",       freq=80),
            ECP5PLLConfig("sync_neg",   freq=80, phase=180),
            ECP5PLLConfig("cic",        freq=40),
        ]

        m.submodules.pll = ECP5PLL(configs)

        return m


class N64CartIO(wiring.Component):
    pi:     In(PISignature)
    si:     In(SISignature)
    cic:    In(CICSignature)
    ctl:    In(CtlSignature)

    def elaborate(self, platform):
        m = Module()

        n64_cart = platform.request("n64_cart")

        pi_ad_i_ff = Signal(16)
        pi_ale_h_ff = Signal()
        pi_ale_l_ff = Signal()
        pi_read_ff = Signal()
        pi_write_ff = Signal()

        m.submodules += [
            cdc.FFSynchronizer(n64_cart.pi.ad.i, pi_ad_i_ff),
            cdc.FFSynchronizer(n64_cart.pi.ale_h.i, pi_ale_h_ff),
            cdc.FFSynchronizer(n64_cart.pi.ale_l.i, pi_ale_l_ff),
            cdc.FFSynchronizer(n64_cart.pi.read.i, pi_read_ff),
            cdc.FFSynchronizer(n64_cart.pi.write.i, pi_write_ff),
        ]

        m.d.comb += [
            # PI
            self.pi.ad.i            .eq( pi_ad_i_ff             ),
            n64_cart.pi.ad.o        .eq( self.pi.ad.o           ),
            n64_cart.pi.ad.oe       .eq( self.pi.ad.oe          ),
            self.pi.ale_h           .eq( pi_ale_h_ff            ),
            self.pi.ale_l           .eq( pi_ale_l_ff            ),
            self.pi.read            .eq( pi_read_ff             ),
            self.pi.write           .eq( pi_write_ff            ),

            # SI
            self.si.data.i          .eq( n64_cart.si.data.i     ),
            n64_cart.si.data.o      .eq( self.si.data.o         ),
            n64_cart.si.data.oe     .eq( self.si.data.oe        ),
            self.si.dclk            .eq( n64_cart.si.dclk.i     ),

            # CIC
            self.cic.data.i         .eq( n64_cart.cic.data.i    ),
            n64_cart.cic.data.o     .eq( self.cic.data.o        ),
            n64_cart.cic.data.oe    .eq( self.cic.data.oe       ),
            self.cic.dclk           .eq( n64_cart.cic.dclk.i    ),

            # Control
            self.ctl.reset          .eq( n64_cart.reset.i       ),
            self.ctl.nmi            .eq( n64_cart.nmi.i         ),
        ]

        return m


class FT245IO(wiring.Component):
    bus: In(ft245.FT245Signature)

    def elaborate(self, platform):
        m = Module()

        usb_ft245 = platform.request("usb_fifo")

        m.d.comb += [
            self.bus.d.i        .eq(usb_ft245.d.i),
            self.bus.rxf        .eq(usb_ft245.rxf.i),
            self.bus.txe        .eq(usb_ft245.txe.i),
            self.bus.clkout     .eq(usb_ft245.clkout.i),

            usb_ft245.d.o       .eq(self.bus.d.o),
            usb_ft245.d.oe      .eq(self.bus.d.oe),
            usb_ft245.rd.o      .eq(self.bus.rd),
            usb_ft245.wr.o      .eq(self.bus.wr),
            usb_ft245.siwu.o    .eq(self.bus.siwu),
            usb_ft245.oe.o      .eq(self.bus.oe),
        ]

        return m


class FlashIO(wiring.Component):
    bus: In(flash.FlashSignature)
    sck: Out(1)

    def elaborate(self, platform):
        m = Module()

        neg_clk = ClockSignal("sync_neg")
        spi_sck = Signal()

        # Dynamically enable or disable primary clock network.
        # Disable function will not create glitch and increase the clock latency.
        m.submodules.dcca = Instance("DCCA",
            i_CE=self.bus.sck_en,
            i_CLKI=neg_clk,
            o_CLKO=spi_sck,
        )

        # Provides access to configuration flash clock (MCLK)
        m.submodules.usrmclk = Instance("USRMCLK",
            i_USRMCLKI=spi_sck,
            i_USRMCLKTS=Const(0),   # Active-low output enable
        )

        qspi_pins = platform.request("qspi_flash")

        m.d.comb += [
            qspi_pins.cs_n.o    .eq(self.bus.cs_n),
            self.sck            .eq(spi_sck)
        ]

        for i in range(4):
            dq_pin = getattr(qspi_pins, f"dq{i}")

            m.d.comb += [
                dq_pin.o        .eq(self.bus.d.o[i]),
                dq_pin.oe       .eq(self.bus.d.oe[i]),

                self.bus.d.i[i] .eq(dq_pin.i),
            ]

        return m


class HomeInvaderRevAPlatform(LatticeECP5Platform):
    device      = "LFE5U-12F"
    package     = "BG256"
    speed       = "6"
    default_clk = "clk12"
    connectors = []

    clock_domain_generator = HomeInvaderRevADomainGenerator

    cart_io = N64CartIO
    ft245_io = FT245IO
    flash_io = FlashIO

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
            Subsignal("d",          Pins("C4 C5 C6 C7 D4 D5 D6 D7", dir="io"))
        ),

        Resource("leds", 0,
            Subsignal("d",          Pins("C16 B16 C15 B15 E15 C14 D14 E14", dir="o")),
        )
    ]

    @property
    def required_tools(self):
        return super().required_tools + [
          "ecpprog"
        ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = {
            "synth_opts": "-abc9",
            "nextpnr_opts": "--seed 0",
            "ecppack_opts": "--compress --freq 38.8",
        }
        return super().toolchain_prepare(fragment, name, **overrides, **kwargs)

    def toolchain_program(self, products, name, **kwargs):
        ecpprog = os.environ.get("ECPPROG", "ecpprog")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call([ecpprog, "-d", "s:0x0403:0x6010:FT5YLSVU", "-I", "B", "-S", bitstream_filename])
