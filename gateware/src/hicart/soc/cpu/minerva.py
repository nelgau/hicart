import warnings

from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth_soc import wishbone
from amaranth_soc.periph import ConstantMap

# Silence record-related deprecation warnings
with warnings.catch_warnings():
    warnings.filterwarnings(action="ignore", category=DeprecationWarning)
    from minerva.core import Minerva

from . import CPU, ConstantAddr


__all__ = ["MinervaCPU"]


class MinervaCPU(CPU, wiring.Component):
    name       = "minerva"
    arch       = "riscv"
    byteorder  = "little"
    data_width = 32

    def __init__(self, **kwargs):
        self._cpu = Minerva(**kwargs)

        wb_signature = wishbone.Signature(addr_width=30, data_width=32, granularity=8,
                                          features={"err", "cti", "bte"})

        super().__init__({
            "ibus": Out(wb_signature),
            "dbus": Out(wb_signature),
            "ip":   In(self._cpu.external_interrupt.shape()),
        })

    @property
    def reset_addr(self):
        return self._cpu.reset_address

    @property
    def muldiv(self):
        return "hard" if self._cpu.with_muldiv else "soft"

    @property
    def constant_map(self):
        return ConstantMap(
            MINERVA           = True,
            RESET_ADDR        = ConstantAddr(self.reset_addr),
            ARCH_RISCV        = True,
            RISCV_MULDIV_SOFT = self.muldiv == "soft",
            BYTEORDER_LITTLE  = True,
        )

    def elaborate(self, platform):
        m = Module()

        m.submodules.minerva = self._cpu

        self.forward_interface(m, self._cpu.ibus, self.ibus)
        self.forward_interface(m, self._cpu.dbus, self.dbus)

        m.d.comb += self._cpu.external_interrupt.eq(self.ip)

        return m

    def forward_interface(self, m, from_bus, to_bus):
        members = to_bus.signature.members
        for name in members:
            from_value = getattr(from_bus, name)
            to_value = getattr(to_bus, name)

            flow = members[name].flow
            if flow == In:
                m.d.comb += from_value.eq(to_value)
            elif flow == Out:
                m.d.comb += to_value.eq(from_value)
