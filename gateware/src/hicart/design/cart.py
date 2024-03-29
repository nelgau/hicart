from amaranth import *
from amaranth.lib import wiring
from amaranth.build import *
from amaranth_soc import wishbone

from hicart.n64.cic import CIC
from hicart.n64.pi import WishboneBridge
from hicart.interface.qspi_flash import QSPIFlashWishboneInterface
from hicart.soc.wishbone import DownConverter, Translator
from hicart.utils.cli import main_runner


class Top(Elaboratable):

    def elaborate(self, platform):
        m = Module()

        leds = platform.get_leds()

        m.submodules.car                               = platform.clock_domain_generator()
        m.submodules.cic        = self.cic = cic       = DomainRenamer("cic")(CIC())

        m.submodules.bridge          = self.bridge          = bridge          = WishboneBridge()
        m.submodules.flash_interface = self.flash_interface = flash_interface = QSPIFlashWishboneInterface()
        m.submodules.flash_connector = self.flash_connector = flash_connector = platform.flash_connector()

        translator = Translator(sub_bus=flash_interface.bus,
                                base_addr=0x800000,
                                addr_width=24,
                                features={"stall"})

        down_converter = DownConverter(sub_bus=translator.bus,
                                       addr_width=23,
                                       data_width=16,
                                       granularity=8,
                                       features={"stall"})

        decoder = wishbone.Decoder(addr_width=31, data_width=16, granularity=8, features={"stall"})
        decoder.add(down_converter.bus, addr=0x10000000)

        m.submodules.translator = translator
        m.submodules.down_converter = down_converter
        m.submodules.decoder = decoder

        n64_cart = self.n64_cart = platform.request('n64_cart')
        pmod     = self.pmod     = platform.request('pmod')

        wiring.connect(m, bridge.wb, decoder.bus)
        wiring.connect(m, flash_interface.qspi, flash_connector.qspi)

        # wiring.connect(m, cic.bus, n64_cart.cic)
        # wiring.connect(m, bridge.pi, n64_cart.pi)

        m.d.comb += [
            cic.bus.dclk.i          .eq( n64_cart.cic.dclk.i    ),
            cic.bus.data.i          .eq( n64_cart.cic.data.i    ),
            n64_cart.cic.data.o     .eq( cic.bus.data.o         ),
            n64_cart.cic.data.oe    .eq( cic.bus.data.oe        ),
        ]

        m.d.comb += [
            bridge.pi.ad.i          .eq( n64_cart.pi.ad.i       ),
            n64_cart.pi.ad.o        .eq( bridge.pi.ad.o         ),
            n64_cart.pi.ad.oe       .eq( bridge.pi.ad.oe        ),
            bridge.pi.ale_h.i       .eq( n64_cart.pi.ale_h.i    ),
            bridge.pi.ale_l.i       .eq( n64_cart.pi.ale_l.i    ),
            bridge.pi.read.i        .eq( n64_cart.pi.read.i     ),
            bridge.pi.write.i       .eq( n64_cart.pi.write.i    ),
        ]

        m.d.comb += [
            cic.reset               .eq( n64_cart.reset.i       ),
            bridge.reset            .eq( n64_cart.reset.i       ),
        ]

        m.d.comb += [
            leds[0]                 .eq( bridge.wb.cyc          ),
            pmod.d.oe               .eq( 1 )
        ]

        m.d.comb += [
            pmod.d.o[0]             .eq( n64_cart.cic.dclk      ),
            pmod.d.o[1]             .eq( n64_cart.cic.data.i    ),
            pmod.d.o[2]             .eq( n64_cart.nmi.i         ),
            pmod.d.o[3]             .eq( n64_cart.pi.read.i     ),
            pmod.d.o[4]             .eq( n64_cart.pi.ale_l.i    ),
            pmod.d.o[5]             .eq( n64_cart.pi.ale_h.i    ),
            pmod.d.o[6]             .eq( n64_cart.si.dclk.i     ),
            pmod.d.o[7]             .eq( n64_cart.si.data.i     ),
        ]

        return m

if __name__ == "__main__":
    main_runner(Top())
