from amaranth import *
from amaranth.lib import wiring
from amaranth.build import *
from amaranth_soc import wishbone

from hicart.n64.cic import CIC
from hicart.n64.pi import WishboneBridge
from hicart.controller.flash import WishboneFlashController
from hicart.soc.wishbone import WindowMapper
from hicart.utils.cli import main_runner


class Top(Elaboratable):

    def elaborate(self, platform):
        m = Module()

        leds = platform.get_leds()

        m.submodules.car                        = platform.clock_domain_generator()
        m.submodules.flash_io   = flash_io      = platform.flash_io()
        m.submodules.cart_io    = cart_io       = platform.cart_io()

        m.submodules.cic        = cic           = DomainRenamer("cic")(CIC())
        m.submodules.bridge     = bridge        = WishboneBridge()
        m.submodules.flash_ctrl = flash_ctrl    = WishboneFlashController(data_width=16)

        mapper = WindowMapper(flash_ctrl.wb, addr_width=22, base_addr=0x800000)

        decoder = wishbone.Decoder(addr_width=31, data_width=16, granularity=8, features={"stall"})
        decoder.add(mapper.bus, addr=0x10000000)

        m.submodules.mapper = mapper
        m.submodules.decoder = decoder

        pmod     = self.pmod     = platform.request("pmod")

        wiring.connect(m, bridge.wb, decoder.bus)
        wiring.connect(m, flash_ctrl.bus, flash_io.bus)

        wiring.connect(m, bridge.pi, cart_io.pi)
        wiring.connect(m, bridge.sys, cart_io.sys)

        wiring.connect(m, cic.bus, cart_io.cic)
        wiring.connect(m, cic.sys, cart_io.sys)

        m.d.sync += [
            pmod.d.o[0]             .eq( cart_io.cic.dclk       ),
            pmod.d.o[1]             .eq( cart_io.cic.data.i     ),
            pmod.d.o[2]             .eq( cart_io.sys.nmi        ),
            pmod.d.o[3]             .eq( cart_io.pi.read        ),
            pmod.d.o[4]             .eq( cart_io.pi.ale_l       ),
            pmod.d.o[5]             .eq( cart_io.pi.ale_h       ),
            pmod.d.o[6]             .eq( cart_io.si.dclk        ),
            pmod.d.o[7]             .eq( cart_io.si.data.i      ),
            pmod.d.oe               .eq( 1 )
        ]

        m.d.sync += [
            leds[0]                 .eq( bridge.wb.cyc          ),
        ]

        return m

if __name__ == "__main__":
    main_runner(Top())
