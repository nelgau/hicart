from amaranth import *

from hicart.sys.mailbox import CommandMailbox
from hicart.sys.sd import SDDataBuffer


class Crossing(Elaboratable):

    def __init__(self, *, host_domain="sync", sys_domain="sync"):
        super().__init__()

        self.mailbox = CommandMailbox(host_domain=host_domain,
                                      sys_domain=sys_domain)

        self.sd_buffer = SDDataBuffer(num_sectors=8,
                                      host_domain=host_domain,
                                      sys_domain=sys_domain)

    def elaborate(self, platform):
        m = Module()

        m.submodules.mailbox = self.mailbox
        m.submodules.sd_buffer = self.sd_buffer

        return m
