from amaranth import *

from hicart.sys.mailbox import CommandMailbox


class Crossing(Elaboratable):

    def __init__(self):
        super().__init__()

        self.mailbox = CommandMailbox()

    def elaborate(self, platform):
        m = Module()

        m.submodules.mailbox = self.mailbox

        return m
