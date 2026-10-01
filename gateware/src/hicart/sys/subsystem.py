from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out, flipped

from hicart.n64.cart import CICSignature, CtlSignature
from hicart.sys.cic import CIC
from hicart.sys.mcu import MCU


class SysSubsystem(wiring.Component):
    cart_cic: Out(CICSignature)
    cart_ctl: Out(CtlSignature)

    def __init__(self, *, crossing):
        self.crossing = crossing

        super().__init__()

        self.mcu = MCU(mailbox_bus=crossing.mailbox.sys_bus)
        self.cic = CIC()


    def elaborate(self, platform):
        m = Module()

        # MCU

        m.submodules.mcu = self.mcu

        # CIC

        m.submodules.cic = self.cic

        wiring.connect(m, self.cic.bus, flipped(self.cart_cic))
        wiring.connect(m, self.cic.ctl, flipped(self.cart_ctl))

        return m
