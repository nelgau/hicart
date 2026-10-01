from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out, flipped
from amaranth_soc import wishbone
from amaranth_soc.csr.wishbone import WishboneCSRBridge
from amaranth_soc.wishbone.sram import WishboneSRAM

from hicart.n64 import cart
from hicart.n64.pi import PISeqBridge
from hicart.controller import flash
from hicart.soc import seqbus
from hicart.soc.wishbone import WindowMapper


class HostSubsystem(wiring.Component):
    cart_pi: Out(cart.PISignature)
    flash: Out(flash.FlashSignature)

    access: Out(1)

    def __init__(self):
        super().__init__()
        self._mailbox_bus = None

    @property
    def mailbox_bus(self):
        return self._mailbox_bus

    @mailbox_bus.setter
    def mailbox_bus(self, bus):
        self._mailbox_bus = bus

    def elaborate(self, platform):
        m = Module()

        # MCU Mailbox

        if self.mailbox_bus is None:
            raise ValueError("Host cannot be elaborated without a mailbox bus")

        csr_bridge = WishboneCSRBridge(self.mailbox_bus, data_width=16)
        m.submodules.csr_bridge = csr_bridge

        # SRAM

        sram = WishboneSRAM(size=0x1000, data_width=16, granularity=8)
        m.submodules.sram = sram

        # Flash

        flash_ctrl = flash.WishboneFlashController(data_width=16)
        mapper = WindowMapper(flash_ctrl.wb, addr_width=22, base_addr=0x800000, name="flash")
        fetcher = seqbus.PrefetchingWishboneBridge(mapper.bus)

        m.submodules.flash_ctrl = flash_ctrl
        m.submodules.mapper = mapper
        m.submodules.fetcher = fetcher

        wiring.connect(m, flash_ctrl.bus, flipped(self.flash))

        # Seqbus-Wishbone Bridge and Decoder

        wb_decoder = wishbone.Decoder(addr_width=19, data_width=16, granularity=8)

        wb_decoder.add(csr_bridge.wb_bus, addr=0x00000)
        wb_decoder.add(sram.wb_bus, addr=0xF0000)

        wb_bridge = seqbus.WishboneBridge(wb_decoder.bus)

        m.submodules.wb_decoder = wb_decoder
        m.submodules.wb_bridge = wb_bridge

        # PI-SeqBus Bridge and Decoder

        seq_decoder = seqbus.Decoder(addr_width=31, data_width=16, granularity=8)
        seq_bridge = PISeqBridge()

        seq_decoder.add(fetcher.seq, addr=0x10000000)
        seq_decoder.add(wb_bridge.seq, addr=0x1FF00000)

        m.submodules.seq_decoder = seq_decoder
        m.submodules.seq_bridge = seq_bridge

        wiring.connect(m, seq_bridge.pi, flipped(self.cart_pi))
        wiring.connect(m, seq_bridge.seq, seq_decoder.bus)

        m.d.comb += self.access.eq(seq_bridge.seq.cyc)

        return m