from amaranth import *
from amaranth.lib import cdc, wiring
from amaranth.lib.wiring import In, Out, flipped

from hicart.controller import sd
from hicart.n64.cart import CICSignature, CtlSignature
from hicart.sys.cic import CIC
from hicart.sys.mcu import MCU


class SysSubsystem(wiring.Component):
    cart_cic: Out(CICSignature)
    cart_ctl: Out(CtlSignature)

    sd_bus: Out(sd.SDBusSignature())

    def __init__(self, *, crossing):
        self.crossing = crossing

        super().__init__()

        self.mcu = MCU(mailbox_bus=crossing.mailbox.sys_bus)
        self.cic = CIC()

        self.sd = sd.SDController(divisor=50, startup_delay=1_000_000)


    def elaborate(self, platform):
        m = Module()

        # MCU

        m.submodules.mcu = self.mcu

        # CIC

        m.submodules.cic = self.cic
        m.submodules += cdc.AsyncFFSynchronizer(self.cart_ctl.reset, self.cic.reset)

        wiring.connect(m, self.cic.bus, flipped(self.cart_cic))

        # SD Controller

        m.submodules.sd = self.sd

        wiring.connect(m, self.sd.bus, flipped(self.sd_bus))

        return m
