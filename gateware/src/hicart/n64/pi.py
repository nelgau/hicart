from amaranth import *
from amaranth_soc import wishbone

from hicart.n64.ad16 import AD16, AD16Interface
from hicart.n64.burst import BurstDecoder, DirectBurst2Wishbone, BufferedBurst2Wishbone


class PIWishboneInitiator(Elaboratable):
    def __init__(self):
        self.bus = wishbone.Interface(addr_width=32, data_width=32, features={"stall"})
        self.ad16 = AD16()

        self.late_block = Signal()
        self.late_read = Signal()

    def elaborate(self, platform):
        m = Module()

        m.submodules.interface = interface = AD16Interface()
        m.submodules.decoder   = decoder   = BurstDecoder()
        m.submodules.direct    = direct    = DirectBurst2Wishbone()
        m.submodules.buffered  = buffered  = BufferedBurst2Wishbone()
        m.submodules.arbiter   = arbiter   = wishbone.Arbiter(addr_width=32, data_width=32, features={"stall"})

        arbiter.add(direct.wbbus)
        arbiter.add(buffered.wbbus)

        m.d.comb += [
            interface.ad16      .connect( self.ad16     ),
            interface.bus       .connect( decoder.bus   ),
            decoder.direct      .connect( direct.bbus   ),
            decoder.buffered    .connect( buffered.bbus ),
            arbiter.bus         .connect( self.bus      ),

            self.late_block     .eq(interface.late_block),
            self.late_read      .eq(interface.late_read),
        ]

        return m
