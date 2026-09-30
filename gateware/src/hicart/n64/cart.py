from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out


PISignature = wiring.Signature({
    "ad":       Out(wiring.Signature({
        "i":    In(16),
        "o":    Out(16),
        "oe":   Out(1),
    })),
    "ale_h":    In(1),
    "ale_l":    In(1),
    "read":     In(1),
    "write":    In(1),
})

SISignature = wiring.Signature({
    "data":     Out(wiring.Signature({
        "i":    In(1),
        "o":    Out(1),
        "oe":   Out(1),
    })),
    "dclk":     In(1),
})

CICSignature = wiring.Signature({
    "data":     Out(wiring.Signature({
        "i":    In(1),
        "o":    Out(1),
        "oe":   Out(1),
    })),
    "dclk":     In(1),
})

CtlSignature = wiring.Signature({
    "reset":    In(1),
    "nmi":      In(1),
})
