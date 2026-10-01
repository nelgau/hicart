from amaranth import *

from hicart.sys.mailbox import CommandMailbox


class Crossing(Elaboratable):

    def __init__(self, *, host_domain="sync", sys_domain="sync"):
        super().__init__()

        self.mailbox = CommandMailbox(host_domain=host_domain, sys_domain=sys_domain)

    def elaborate(self, platform):
        m = Module()

        m.submodules.mailbox = self.mailbox

        return m
