from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import Out

from hicart.utils.plat import pin_signature


PISignature = wiring.Signature({
    "ad":       Out(pin_signature(16, "io")),
    "ale_h":    Out(pin_signature(1, "i")),
    "ale_l":    Out(pin_signature(1, "i")),
    "read":     Out(pin_signature(1, "i")),
    "write":    Out(pin_signature(1, "i")),
})

SISignature = wiring.Signature({
    "dclk":     Out(pin_signature(1, "i")),
    "data":     Out(pin_signature(1, "io")),
})

CICSignature = wiring.Signature({
    "dclk":     Out(pin_signature(1, "i")),
    "data":     Out(pin_signature(1, "io")),
})

CartBusSignature = wiring.Signature({
    "pi":       Out(PISignature),
    "si":       Out(SISignature),
    "cic":      Out(CICSignature),

    "reset":    Out(pin_signature(1, "i")),
    "nmi":      Out(pin_signature(1, "i")),
})
