from amaranth import *
from amaranth.lib import cdc, wiring
from amaranth.lib.wiring import In, Out, flipped
from amaranth.utils import exact_log2

from hicart.controller import sd
from hicart.n64.cart import CICSignature, CtlSignature
from hicart.sys.cic import CIC
from hicart.sys.mcu import MCU
from hicart.sys.sd import SDBufferWriter


class SysSubsystem(wiring.Component):
    cart_cic: Out(CICSignature)
    cart_ctl: Out(CtlSignature)

    sd_bus: Out(sd.BusSignature())

    def __init__(self, *, crossing):
        self.crossing = crossing
        super().__init__()

        self.mcu = MCU(mailbox_bus=crossing.mailbox.sys_bus)
        self.cic = CIC()

        sd_config = sd.ControllerConfig(clk_freq=40e6)
        self.sd_periph = sd.Peripheral(config=sd_config)

        self.writer = SDBufferWriter(writer_bus=crossing.sd_buffer.writer_bus)

    def elaborate(self, platform):
        m = Module()

        # MCU

        m.submodules.mcu = self.mcu

        # CIC

        m.submodules.cic = self.cic
        m.submodules += cdc.AsyncFFSynchronizer(self.cart_ctl.reset, self.cic.reset)

        wiring.connect(m, self.cic.bus, flipped(self.cart_cic))

        # SD Controller

        m.submodules.sd_periph = self.sd_periph
        m.submodules.writer = self.writer

        wiring.connect(m, self.sd_periph.sd_bus, flipped(self.sd_bus))

        wiring.connect(m, self.sd_periph.source, self.writer.sink)
        wiring.connect(m, self.writer.writer_bus, self.crossing.sd_buffer.writer_bus)

        return m
