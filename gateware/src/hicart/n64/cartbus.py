from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.cdc import FFSynchronizer
from amaranth.lib.wiring import In, Out, Signature

from hicart.utils.plat import TristateSignature


PISignature = wiring.Signature({
    "ad":       Out(TristateSignature(16)),
    "ale_h":    In(1),
    "ale_l":    In(1),
    "read":     In(1),
    "write":    In(1),
})

SISignature = wiring.Signature({
    "dclk":     In(1),
    "data":     Out(TristateSignature(1)),
})

CICSignature = wiring.Signature({
    "dclk":     Out(Signature({"i": In(1)})),
    "data":     Out(TristateSignature(1)),
})

CartBusSignature = wiring.Signature({
    "pi":       Out(PISignature),
    "si":       Out(SISignature),
    "cic":      Out(CICSignature),

    "reset":    In(1),
    "nmi":      In(1),
})
