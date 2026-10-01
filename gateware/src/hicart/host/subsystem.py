from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out, flipped
from amaranth_soc.wishbone.sram import WishboneSRAM

from hicart.n64 import cart
from hicart.n64.pi import PISeqBridge
from hicart.controller import flash
from hicart.soc import seqbus
from hicart.soc.wishbone import WindowMapper


class HostSubsystem(wiring.Component):
    pi: Out(cart.PISignature)
    flash: Out(flash.FlashSignature)

    access: Out(1)

    def elaborate(self, platform):
        m = Module()

        # Flash

        flash_ctrl = flash.WishboneFlashController(data_width=16)
        mapper = WindowMapper(flash_ctrl.wb, addr_width=22, base_addr=0x800000, name="flash")
        fetcher = seqbus.PrefetchingWishboneBridge(mapper.bus)

        m.submodules.flash_ctrl = flash_ctrl
        m.submodules.mapper = mapper
        m.submodules.fetcher = fetcher

        wiring.connect(m, flash_ctrl.bus, flipped(self.flash))

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

        m.submodules.decoder = decoder
        m.submodules.bridge = bridge

        wiring.connect(m, bridge.pi, flipped(self.pi))
        wiring.connect(m, bridge.seq, decoder.bus)

        m.d.comb += self.access.eq(bridge.seq.cyc)

        return m