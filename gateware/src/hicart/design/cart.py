from amaranth import *
from amaranth.build import *
from amaranth_soc import wishbone

from hicart.n64.cic import CIC
from hicart.n64.pi import PIWishboneInitiator
from hicart.interface.qspi_flash import QSPIFlashWishboneInterface
from hicart.soc.wishbone import DownConverter, Translator
from hicart.utils.cli import main_runner


class Top(Elaboratable):

    def elaborate(self, platform):
        m = Module()

        leds = platform.get_leds()

        m.submodules.car                               = platform.clock_domain_generator()
        m.submodules.cic        = self.cic = cic       = DomainRenamer("cic")(CIC())
        
        m.submodules.initiator       = self.initiator       = initiator       = PIWishboneInitiator();
        m.submodules.flash_interface = self.flash_interface = flash_interface = QSPIFlashWishboneInterface()
        m.submodules.flash_connector = self.flash_connector = flash_connector = platform.flash_connector()

        translator = Translator(sub_bus=flash_interface.bus,
                                base_addr=0x800000,
                                addr_width=24,
                                features={"stall"})

        down_converter = DownConverter(sub_bus=translator.bus,
                                       addr_width=22,
                                       data_width=32,
                                       granularity=8,
                                       features={"stall"})

        decoder = wishbone.Decoder(addr_width=32, data_width=32, granularity=8, features={"stall"})
        decoder.add(down_converter.bus, addr=0x10000000)

        m.submodules.translator = translator
        m.submodules.down_converter = down_converter
        m.submodules.decoder = decoder








        n64_cart = self.n64_cart = platform.request('n64_cart')
        pmod     = self.pmod     = platform.request('pmod')

        m.d.comb += [
            cic.reset               .eq( n64_cart.reset      ),
            cic.data_clk            .eq( n64_cart.cic_dclk   ),
            cic.data_i              .eq( n64_cart.cic_data.i ),

            n64_cart.cic_data.o     .eq( cic.data_o  ),
            n64_cart.cic_data.oe    .eq( cic.data_oe ),
        ]

        m.d.comb += [
            initiator.bus           .connect(decoder.bus),
            flash_interface.qspi    .connect(flash_connector.qspi),            

            initiator.ad16.ad.i     .eq( n64_cart.ad.i  ),
            initiator.ad16.ale_h    .eq( n64_cart.ale_h ),
            initiator.ad16.ale_l    .eq( n64_cart.ale_l ),
            initiator.ad16.read     .eq( n64_cart.read  ),
            initiator.ad16.write    .eq( n64_cart.write ),

            n64_cart.ad.o           .eq( initiator.ad16.ad.o  ),
            n64_cart.ad.oe          .eq( initiator.ad16.ad.oe ),

            pmod.d.oe               .eq(1)
        ]

        m.d.comb += [
            leds[0]                 .eq(initiator.bus.cyc),
        ]

        self.probe_si(m)

        return m

    def probe_initiator_addr(self, m):
        initiator = self.initiator
        pmod = self.pmod
        m.d.comb += pmod.d.o.eq(initiator.bus.adr[0:8])

    def probe_initiator_bus(self, m):
        initiator = self.initiator
        flash_interface = self.flash_interface
        pmod = self.pmod
        m.d.comb += [
            pmod.d.o[0].eq(initiator.bus.cyc),
            pmod.d.o[1].eq(initiator.bus.stb),
            pmod.d.o[2].eq(initiator.bus.stall),
            pmod.d.o[3].eq(initiator.bus.ack),

            pmod.d.o[4].eq(flash_interface.bus.cyc),
            pmod.d.o[5].eq(flash_interface.bus.stb),
            pmod.d.o[6].eq(flash_interface.bus.stall), 
            pmod.d.o[7].eq(flash_interface.bus.ack), 
        ]

    def probe_bus_and_initiator(self, m):
        n64_cart = self.n64_cart
        initiator = self.initiator
        pmod = self.pmod
        m.d.comb += [
            pmod.d.o[0].eq(n64_cart.cic_data.i),
            pmod.d.o[1].eq(n64_cart.read),            
            pmod.d.o[2].eq(n64_cart.ale_l),
            pmod.d.o[3].eq(n64_cart.ale_h),

            pmod.d.o[4].eq(initiator.bus.cyc),
            pmod.d.o[5].eq(initiator.bus.stb),
            pmod.d.o[6].eq(initiator.bus.stall),
            pmod.d.o[7].eq(initiator.bus.ack),
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
            pmod.d.o[0].eq(n64_cart.cic_data.i),
            pmod.d.o[1].eq(n64_cart.read),            
            pmod.d.o[2].eq(n64_cart.ale_l),
            pmod.d.o[3].eq(n64_cart.ale_h),
            pmod.d.o[4].eq(n64_cart.ad.i[15]),
            pmod.d.o[5].eq(n64_cart.ad.i[14]),
            pmod.d.o[6].eq(n64_cart.ad.i[13]),
            pmod.d.o[7].eq(n64_cart.ad.i[12]),
        ]

    def probe_cic(self, m):
        n64_cart = self.n64_cart
        pmod = self.pmod
        m.d.comb += [
            pmod.d.o[0].eq(n64_cart.cic_dclk),
            pmod.d.o[1].eq(n64_cart.cic_data.i),
            pmod.d.o[2].eq(n64_cart.nmi),
            pmod.d.o[3].eq(n64_cart.read),          
            pmod.d.o[4].eq(n64_cart.ale_l),
            pmod.d.o[5].eq(n64_cart.ale_h),
            pmod.d.o[6].eq(n64_cart.ad.i[15]),
            pmod.d.o[7].eq(n64_cart.ad.i[14]),
        ]

    def probe_si(self, m):
        n64_cart = self.n64_cart
        pmod = self.pmod
        m.d.comb += [
            pmod.d.o[0].eq(n64_cart.cic_dclk),
            pmod.d.o[1].eq(n64_cart.cic_data.i),
            pmod.d.o[2].eq(n64_cart.nmi),
            pmod.d.o[3].eq(n64_cart.read),          
            pmod.d.o[4].eq(n64_cart.ale_l),
            pmod.d.o[5].eq(n64_cart.ale_h),
            pmod.d.o[6].eq(n64_cart.s_clk),
            pmod.d.o[7].eq(n64_cart.s_data),
        ]        

    def probe_ad_low(self, m):
        n64_cart = self.n64_cart
        pmod = self.pmod
        m.d.comb += [
            pmod.d.o.eq(n64_cart.ad.i[8:16]),
        ]

    def probe_ad_high(self, m):
        n64_cart = self.n64_cart
        pmod = self.pmod
        m.d.comb += [
            pmod.d.o.eq(n64_cart.ad.i[8:16]),
        ]

if __name__ == "__main__":
    main_runner(Top())
