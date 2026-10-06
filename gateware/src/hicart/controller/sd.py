from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out


class SDBusSignature(wiring.Signature):
    def __init__(self):
        super().__init__({
            "clk": Out(1),
            "cmd": Out(wiring.Signature({
                "i":    In(1),
                "o":    Out(1),
                "oe":   Out(1),
            })),
            "dat": Out(wiring.Signature({
                "i":    In(4),
                "o":    Out(4),
                "oe":   Out(4),
            })),
            "card_present": In(1),
        })
