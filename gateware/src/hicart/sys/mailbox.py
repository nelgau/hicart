from amaranth import *
from amaranth.lib import cdc, wiring
from amaranth.lib.wiring import In, Out, flipped
from amaranth.utils import exact_log2
from amaranth_soc import csr


class CommandMailbox(wiring.Component):

    class HostHandshake(csr.Register, access="r"):
        def __init__(self, data_width):
            super().__init__({
                "busy":     csr.Field(csr.action.R, unsigned(1)),
                "error":    csr.Field(csr.action.R, unsigned(1)),
                "_0":       csr.Field(csr.action.R, unsigned(data_width - 2))
            })

    class SysHandshake(csr.Register, access="rw"):
        def __init__(self, data_width):
            super().__init__({
                "pending":  csr.Field(csr.action.R, unsigned(1)),
                "error":    csr.Field(csr.action.RW, unsigned(1)),
                "_0":       csr.Field(csr.action.R, unsigned(data_width - 2))
            })

    class ValueRW(csr.Register, access="rw"):
        def __init__(self, shape):
            super().__init__({
                "value": csr.Field(csr.action.RW, shape)
            })

    class ValueR(csr.Register, access="r"):
        def __init__(self, shape):
            super().__init__({
                "value": csr.Field(csr.action.R, shape)
            })

    def __init__(self, host_domain="sync", sys_domain="sync"):
        self._host_domain = host_domain
        self._sys_domain = sys_domain

        # Host

        host_regs = csr.Builder(addr_width=8, data_width=8)

        self._host_handshake_reg    = host_regs.add("Handshake",    self.HostHandshake(32))
        self._host_command_reg      = host_regs.add("Command",      self.ValueRW(32))
        self._host_arg1_reg         = host_regs.add("Arg1",         self.ValueRW(32))
        self._host_arg2_reg         = host_regs.add("Arg2",         self.ValueRW(32))
        self._host_result_reg       = host_regs.add("Result",       self.ValueR(32))

        # Sys

        sys_regs = csr.Builder(addr_width=8, data_width=8)

        self._sys_handshake_reg     = sys_regs.add("Handshake",     self.SysHandshake(32))
        self._sys_command_reg       = sys_regs.add("Command",       self.ValueR(32))
        self._sys_arg1_reg          = sys_regs.add("Arg1",          self.ValueR(32))
        self._sys_arg2_reg          = sys_regs.add("Arg2",          self.ValueR(32))
        self._sys_result_reg        = sys_regs.add("Result",        self.ValueRW(32))

        # Bridges

        self._host_bridge = DomainRenamer(host_domain)(csr.Bridge(host_regs.as_memory_map()))
        self._sys_bridge = DomainRenamer(sys_domain)(csr.Bridge(sys_regs.as_memory_map()))

        super().__init__({
            "host_bus": In(csr.Signature(addr_width=8, data_width=8)),
            "sys_bus": In(csr.Signature(addr_width=8, data_width=8)),
        })
        self.host_bus.memory_map = self._host_bridge.bus.memory_map
        self.sys_bus.memory_map = self._sys_bridge.bus.memory_map

    def elaborate(self, platform):
        m = Module()

        m.submodules.host_bridge = self._host_bridge
        m.submodules.sys_bridge = self._sys_bridge

        wiring.connect(m, flipped(self.host_bus), self._host_bridge.bus)
        wiring.connect(m, flipped(self.sys_bus), self._sys_bridge.bus)

        send_doorbell = cdc.PulseSynchronizer(i_domain=self._host_domain, o_domain=self._sys_domain)
        done_doorbell = cdc.PulseSynchronizer(i_domain=self._sys_domain, o_domain=self._host_domain)

        m.submodules.send_doorbell = send_doorbell
        m.submodules.done_doorbell = done_doorbell

        m.d.comb += [
            send_doorbell.i.eq(0),
            done_doorbell.i.eq(0),
        ]

        # Host

        host_busy = Signal()
        host_error = Signal()
        host_result = Signal(32)

        with m.If(self._host_command_reg.element.w_stb & ~host_busy):
            m.d.comb += send_doorbell.i.eq(1)
            m.d[self._host_domain] += [
                host_busy.eq(1),
                host_error.eq(0),
            ]

        with m.If(done_doorbell.o):
            m.d[self._host_domain] += [
                host_busy.eq(0),
                host_error.eq(self._sys_handshake_reg.f.error.data),
                host_result.eq(self._sys_result_reg.f.value.data),
            ]

        m.d.comb += [
            self._host_handshake_reg.f.busy.r_data.eq(host_busy),
            self._host_handshake_reg.f.error.r_data.eq(host_error),
            self._host_result_reg.f.value.r_data.eq(host_result),
        ]

        # Sys

        sys_pending = Signal()
        sys_command = Signal(32)
        sys_arg1 = Signal(32)
        sys_arg2 = Signal(32)

        with m.If(self._sys_handshake_reg.element.w_stb & sys_pending):
            m.d.comb += done_doorbell.i.eq(1)
            m.d[self._sys_domain] += [
                sys_pending.eq(0),
            ]

        with m.If(send_doorbell.o):
            m.d[self._sys_domain] += [
                sys_pending.eq(1),

                sys_command.eq(self._host_command_reg.f.value.data),
                sys_arg1.eq(self._host_arg1_reg.f.value.data),
                sys_arg2.eq(self._host_arg2_reg.f.value.data),
            ]

        m.d.comb += [
            self._sys_handshake_reg.f.pending.r_data.eq(sys_pending),
            self._sys_command_reg.f.value.r_data.eq(sys_command),
            self._sys_arg1_reg.f.value.r_data.eq(sys_arg1),
            self._sys_arg2_reg.f.value.r_data.eq(sys_arg2),
        ]

        return m
