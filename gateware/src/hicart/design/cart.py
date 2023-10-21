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

        self.probe_si(m)

        return m

    def probe_bridge_addr(self, m):
        bridge = self.bridge
        pmod = self.pmod
        m.d.comb += pmod.d.o.eq(bridge.bus.adr[0:8])

    def probe_bridge_bus(self, m):
        bridge = self.bridge
        flash_interface = self.flash_interface
        pmod = self.pmod
        m.d.comb += [
            pmod.d.o[0].eq(bridge.wb.cyc),
            pmod.d.o[1].eq(bridge.wb.stb),
            pmod.d.o[2].eq(bridge.wb.stall),
            pmod.d.o[3].eq(bridge.wb.ack),

            pmod.d.o[4].eq(flash_interface.bus.cyc),
            pmod.d.o[5].eq(flash_interface.bus.stb),
            pmod.d.o[6].eq(flash_interface.bus.stall),
            pmod.d.o[7].eq(flash_interface.bus.ack),
        ]

    def probe_bus_and_bridge(self, m):
        n64_cart = self.n64_cart
        bridge = self.bridge
        pmod = self.pmod
        m.d.comb += [
            pmod.d.o[0].eq(n64_cart.cic.data.i),
            pmod.d.o[1].eq(n64_cart.pi.read),
            pmod.d.o[2].eq(n64_cart.pi.ale_l),
            pmod.d.o[3].eq(n64_cart.pi.ale_h),

            pmod.d.o[4].eq(bridge.wb.cyc),
            pmod.d.o[5].eq(bridge.wb.stb),
            pmod.d.o[6].eq(bridge.wb.stall),
            pmod.d.o[7].eq(bridge.wb.ack),
        ]

    def probe_flash_connector(self, m):
        flash_connector = self.flash_connector
        pmod = self.pmod
        m.d.comb += [
            pmod.d.o[0].eq(ClockSignal('sync')),
            pmod.d.o[1].eq(flash_connector.qspi.cs_n),
            pmod.d.o[2].eq(flash_connector.spi_clk),

            pmod.d.o[3].eq(flash_connector.qspi.d.i[0]),
            pmod.d.o[4].eq(flash_connector.qspi.d.i[1]),
            pmod.d.o[5].eq(flash_connector.qspi.d.i[2]),
            pmod.d.o[6].eq(flash_connector.qspi.d.i[3]),
            pmod.d.o[7].eq(flash_connector.qspi.d.oe[0]),
        ]

    def probe_bus_states(self, m):
        n64_cart = self.n64_cart
        pmod = self.pmod
        m.d.comb += [
            pmod.d.o[0].eq(n64_cart.cic.data.i),
            pmod.d.o[1].eq(n64_cart.pi.read),
            pmod.d.o[2].eq(n64_cart.pi.ale_l),
            pmod.d.o[3].eq(n64_cart.pi.ale_h),
            pmod.d.o[4].eq(n64_cart.pi.ad.i[15]),
            pmod.d.o[5].eq(n64_cart.pi.ad.i[14]),
            pmod.d.o[6].eq(n64_cart.pi.ad.i[13]),
            pmod.d.o[7].eq(n64_cart.pi.ad.i[12]),
        ]

    def probe_cic(self, m):
        n64_cart = self.n64_cart
        pmod = self.pmod
        m.d.comb += [
            pmod.d.o[0].eq(n64_cart.cic.dclk),
            pmod.d.o[1].eq(n64_cart.cic.data.i),
            pmod.d.o[2].eq(n64_cart.nmi),
            pmod.d.o[3].eq(n64_cart.pi.read),
            pmod.d.o[4].eq(n64_cart.pi.ale_l),
            pmod.d.o[5].eq(n64_cart.pi.ale_h),
            pmod.d.o[6].eq(n64_cart.pi.ad.i[15]),
            pmod.d.o[7].eq(n64_cart.pi.ad.i[14]),
        ]

    def probe_si(self, m):
        n64_cart = self.n64_cart
        pmod = self.pmod
        m.d.comb += [
            pmod.d.o[0].eq(n64_cart.cic.dclk),
            pmod.d.o[1].eq(n64_cart.cic.data.i),
            pmod.d.o[2].eq(n64_cart.nmi),
            pmod.d.o[3].eq(n64_cart.pi.read),
            pmod.d.o[4].eq(n64_cart.pi.ale_l),
            pmod.d.o[5].eq(n64_cart.pi.ale_h),
            pmod.d.o[6].eq(n64_cart.si.dclk),
            pmod.d.o[7].eq(n64_cart.si.data.i),
        ]        

    def probe_ad_low(self, m):
        n64_cart = self.n64_cart
        pmod = self.pmod
        m.d.comb += [
            pmod.d.o.eq(n64_cart.pi.ad.i[8:16]),
        ]

    def probe_ad_high(self, m):
        n64_cart = self.n64_cart
        pmod = self.pmod
        m.d.comb += [
            pmod.d.o.eq(n64_cart.pi.ad.i[8:16]),
        ]

if __name__ == "__main__":
    main_runner(Top())
