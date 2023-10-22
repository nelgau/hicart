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

        wiring.connect(m, cic.bus, n64_cart.cic)
        wiring.connect(m, bridge.pi, n64_cart.pi)

        m.d.comb += [
            cic.reset               .eq( n64_cart.reset.i    ),
            bridge.reset            .eq( n64_cart.reset.i    ),
        ]

        m.d.comb += [
            leds[0]                 .eq(bridge.wb.cyc),
            pmod.d.oe               .eq(1)
        ]

        return m

if __name__ == "__main__":
    main_runner(Top())
