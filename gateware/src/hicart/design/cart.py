from amaranth import *
from amaranth.lib import wiring
from amaranth.build import *
from amaranth_soc.wishbone.sram import WishboneSRAM

from hicart.n64.cic import CIC
from hicart.n64.pi import PISeqBridge
from hicart.controller import flash
from hicart.soc import seqbus
from hicart.soc.wishbone import WindowMapper
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

        # Flash

        flash_ctrl = flash.WishboneFlashController(data_width=16)

        mapper = WindowMapper(flash_ctrl.wb, addr_width=22, base_addr=0x800000, name="flash")
        fetcher = seqbus.PrefetchingWishboneBridge(mapper.bus)

        wiring.connect(m, flash_ctrl.bus, flash_io.bus)

        m.submodules.flash_ctrl = flash_ctrl
        m.submodules.mapper = mapper
        m.submodules.fetcher = fetcher

        # SRAM

        sram = WishboneSRAM(size=0x1000, data_width=16, granularity=8)
        sram_b = seqbus.WishboneBridge(sram.wb_bus)

        m.submodules.sram = sram
        m.submodules.sram_b = sram_b

        # Bridge and Decoder

        decoder = seqbus.Decoder(addr_width=31, data_width=16, granularity=8)
        decoder.add(fetcher.seq, addr=0x10000000)
        decoder.add(sram_b.seq, addr=0x1FFF0000)

        bridge = PISeqBridge()

        wiring.connect(m, bridge.pi, cart_io.pi)
        wiring.connect(m, bridge.seq, decoder.bus)

        m.submodules.decoder = decoder
        m.submodules.bridge = bridge

        # CIC

        cic = DomainRenamer("cic")(CIC())

        wiring.connect(m, cic.bus, cart_io.cic)
        wiring.connect(m, cic.ctl, cart_io.ctl)

        m.submodules.cic = cic

        # Debug

        pmod = platform.request("pmod")
        leds = platform.request("leds")

        m.d.comb += [
            pmod.d.o[0]             .eq( cart_io.pi.read        ),
            pmod.d.o[1]             .eq( cart_io.pi.write       ),
            pmod.d.o[2]             .eq( cart_io.pi.ale_l       ),
            pmod.d.o[3]             .eq( cart_io.pi.ale_h       ),
            pmod.d.o[4]             .eq( bridge.seq.cyc         ),
            pmod.d.o[5]             .eq( bridge.seq.stb         ),
            pmod.d.o[6]             .eq( bridge.seq.ack         ),
            pmod.d.o[7]             .eq( bridge.seq.err         ),
            pmod.d.oe               .eq( 1 ),

            leds.d.o[0]             .eq( bridge.seq.cyc         ),
        ]

        return m

if __name__ == "__main__":
    main_runner(Top())
