from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import Out
from amaranth_soc import wishbone

from hicart.n64 import ad16
from hicart.n64.burst import BurstDecoder, DirectBurst2Wishbone, BufferedBurst2Wishbone


class PIWishboneInitiator(wiring.Component):
    ad16:           Out(ad16.Signature())
    bus:            Out(wishbone.Signature(addr_width=30, data_width=32, granularity=8, features={"stall"}))
    late_block:     Out(1)
    late_read:      Out(1)

    def elaborate(self, platform):
        m = Module()

        m.submodules.bridge     = bridge    = ad16.BurstBridge()
        m.submodules.decoder    = decoder   = BurstDecoder()
        m.submodules.direct     = direct    = DirectBurst2Wishbone()
        m.submodules.buffered   = buffered  = BufferedBurst2Wishbone()
        m.submodules.arbiter    = arbiter   = wishbone.Arbiter(addr_width=30, data_width=32, granularity=8, features={"stall"})

        arbiter.add(direct.wbbus)
        arbiter.add(buffered.wbbus)

        wiring.connect(m, bridge.ad16,      wiring.flipped(self.ad16))
        wiring.connect(m, bridge.bus,       decoder.bus)
        wiring.connect(m, decoder.direct,   direct.bbus)
        wiring.connect(m, decoder.buffered, buffered.bbus)
        wiring.connect(m, arbiter.bus,      wiring.flipped(self.bus))

        m.d.comb += [
            self.late_block     .eq(bridge.late_block),
            self.late_read      .eq(bridge.late_read),
        ]

        return m
