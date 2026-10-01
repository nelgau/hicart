from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out, flipped

from hicart.n64.cart import CICSignature, CtlSignature
from hicart.n64.cic import CIC


class SysSubsystem(wiring.Component):
    cart_cic: Out(CICSignature)
    cart_ctl: Out(CtlSignature)

    def elaborate(self, platform):
        m = Module()

        # CIC

        cic = CIC()
        m.submodules.cic = cic

        wiring.connect(m, cic.bus, flipped(self.cart_cic))
        wiring.connect(m, cic.ctl, flipped(self.cart_ctl))

        return m
