from amaranth import *
from amaranth.lib import wiring

from hicart.host.subsystem import HostSubsystem
from hicart.sys.crossing import Crossing
from hicart.sys.subsystem import SysSubsystem
from hicart.utils.cli import main_runner


class Top(Elaboratable):

    def elaborate(self, platform):
        m = Module()

        # Platform

        cdg  = platform.clock_domain_generator()
        cart_io = platform.cart_io()
        flash_io = platform.flash_io()
        card_io = platform.card_io()

        m.submodules.cdg = cdg
        m.submodules.cart_io = cart_io
        m.submodules.flash_io = flash_io
        m.submodules.card_io = card_io

        # Subsystems

        crossing = Crossing(host_domain="sync", sys_domain="cic")

        host_subsystem = HostSubsystem(crossing=crossing)
        sys_subsystem = SysSubsystem(crossing=crossing)

        host_subsystem = DomainRenamer("sync")(host_subsystem)
        sys_subsystem = DomainRenamer("cic")(sys_subsystem)

        m.submodules.crossing = crossing
        m.submodules.host_subsystem = host_subsystem
        m.submodules.sys_subsystem = sys_subsystem

        # Connections

        wiring.connect(m, host_subsystem.cart_pi, cart_io.pi)
        wiring.connect(m, host_subsystem.flash, flash_io.bus)

        wiring.connect(m, sys_subsystem.cart_cic, cart_io.cic)
        wiring.connect(m, sys_subsystem.cart_ctl, cart_io.ctl)
        wiring.connect(m, sys_subsystem.sd_bus, card_io.bus)

        # Debug

        pmod = platform.request("pmod")
        leds = platform.request("leds")

        m.d.comb += [
            pmod.d.o[0]             .eq( card_io.bus.clk            ),
            pmod.d.o[1]             .eq( card_io.bus.cmd.i          ),
            pmod.d.o[2]             .eq( card_io.bus.cmd.o          ),
            pmod.d.o[3]             .eq( card_io.bus.cmd.oe         ),
            pmod.d.o[4]             .eq( card_io.bus.dat.i[0]       ),
            pmod.d.o[5]             .eq( card_io.bus.dat.i[1]       ),
            pmod.d.o[6]             .eq( card_io.bus.dat.i[2]       ),
            pmod.d.o[7]             .eq( card_io.bus.dat.i[3]       ),
            pmod.d.oe               .eq( 1 ),

            leds.d.o[0]             .eq( host_subsystem.access      ),
            leds.d.o[7]             .eq( card_io.bus.card_present   ),
        ]

        return m

if __name__ == "__main__":
    main_runner(Top())
