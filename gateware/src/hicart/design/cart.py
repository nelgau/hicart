from amaranth import *
from amaranth.lib import wiring
from amaranth.build import *

from hicart.host.subsystem import HostSubsystem
from hicart.n64.cic import CIC
from hicart.utils.cli import main_runner


class Top(Elaboratable):

    def elaborate(self, platform):
        m = Module()

        # Platform

        cdg  = platform.clock_domain_generator()
        flash_io = platform.flash_io()
        cart_io = platform.cart_io()

        m.submodules.cdg = cdg
        m.submodules.flash_io = flash_io
        m.submodules.cart_io = cart_io

        # Host Subsystem

        host_subsystem = DomainRenamer("sync")(HostSubsystem())
        m.submodules.host_subsystem = host_subsystem

        # CIC

        cic = DomainRenamer("cic")(CIC())
        m.submodules.cic = cic

        # Connections

        wiring.connect(m, host_subsystem.pi, cart_io.pi)
        wiring.connect(m, host_subsystem.flash, flash_io.bus)

        wiring.connect(m, cic.bus, cart_io.cic)
        wiring.connect(m, cic.ctl, cart_io.ctl)

        # Debug

        pmod = platform.request("pmod")
        leds = platform.request("leds")

        m.d.comb += [
            pmod.d.o[0]             .eq( cart_io.pi.read        ),
            pmod.d.o[1]             .eq( cart_io.pi.write       ),
            pmod.d.o[2]             .eq( cart_io.pi.ale_l       ),
            pmod.d.o[3]             .eq( cart_io.pi.ale_h       ),
            pmod.d.o[4]             .eq( 0                      ),
            pmod.d.o[5]             .eq( 0                      ),
            pmod.d.o[6]             .eq( 0                      ),
            pmod.d.o[7]             .eq( 0                      ),
            pmod.d.oe               .eq( 1 ),

            leds.d.o[0]             .eq( host_subsystem.access  ),
        ]

        return m

if __name__ == "__main__":
    main_runner(Top())
