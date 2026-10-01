from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out, flipped
from amaranth_soc import csr

from hicart.n64.cart import CICSignature, CtlSignature
from hicart.n64.cic import CIC
from hicart.sys.mailbox import CommandMailbox


class SysSubsystem(wiring.Component):
    cart_cic: Out(CICSignature)
    cart_ctl: Out(CtlSignature)

    def __init__(self):
        super().__init__()

        self._mailbox = CommandMailbox()

    @property
    def mailbox_bus(self):
        return self._mailbox.host_bus

    def elaborate(self, platform):
        m = Module()

        # MCU Mailbox

        m.submodules.mailbox = self._mailbox

        # CIC

        cic = CIC()
        m.submodules.cic = cic

        wiring.connect(m, cic.bus, flipped(self.cart_cic))
        wiring.connect(m, cic.ctl, flipped(self.cart_ctl))

        return m
