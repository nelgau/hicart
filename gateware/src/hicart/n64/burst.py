from amaranth import *
from amaranth.sim import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth_soc import wishbone


class Signature(wiring.Signature):
    def __init__(self):
        super().__init__({
            # Block
            "blk":          Out(1),
            "base":         Out(32),
            "load":         Out(1),
            "blk_stall":    In(1),
            # Transfer
            "off":          Out(8),
            "dat_w":        Out(32),
            "dat_r":        In(32),
            "cyc":          Out(1),
            "stb":          Out(1),
            "we":           Out(1),
            "stall":        In(1),
            "ack":          In(1),
        })


class _AddressGenerator(wiring.Component):
    base:       In(30)
    offset:     In(30)
    addr:       Out(30)

    def elaborate(self, platform):
        m = Module()

        m.d.comb += [
            self.addr[0:8]  .eq((self.base[0:8] + self.offset)[0:8]),
            self.addr[8:30] .eq(self.base[8:30])
        ]

        return m


class BurstDecoder(wiring.Component):
    bus:        In(Signature())
    direct:     Out(Signature())
    buffered:   Out(Signature())

    def elaborate(self, platform):
        m = Module()

        # wiring.connect(self.bus, self.direct)
        wiring.connect(m, wiring.flipped(self.bus), wiring.flipped(self.buffered))

        return m


class DirectBurst2Wishbone(wiring.Component):
    """ Pass-through burst to Wishbone adapter """
    bbus:       In(Signature())
    wbbus:      Out(wishbone.Signature(addr_width=30, data_width=32, granularity=8, features={"stall"}))

    def elaborate(self, platform):
        m = Module()

        m.submodules.agen = agen = _AddressGenerator()

        m.d.comb += [
            agen.base           .eq(self.bbus.base),
            agen.offset         .eq(self.bbus.off),

            self.wbbus.sel      .eq(Value.cast(1).replicate(4)),

            self.wbbus.cyc      .eq(self.bbus.cyc),
            self.wbbus.stb      .eq(self.bbus.stb),
            self.wbbus.we       .eq(self.bbus.we),
            self.bbus.stall     .eq(self.wbbus.stall),
            self.bbus.ack       .eq(self.wbbus.ack),

            self.wbbus.adr      .eq(agen.addr),
            self.wbbus.dat_w    .eq(self.bbus.dat_w),
            self.bbus.dat_r     .eq(self.wbbus.dat_r),
        ]

        return m


class BufferedBurst2Wishbone(wiring.Component):
    """ Buffered burst to Wishbone adapter """
    bbus:       In(Signature())
    wbbus:      Out(wishbone.Signature(addr_width=30, data_width=32, granularity=8, features={"stall"}))

    def elaborate(self, platform):
        m = Module()

        storage = Memory(width=32, depth=128)

        m.submodules.agen   = agen   = _AddressGenerator()
        m.submodules.w_port = w_port = storage.write_port()
        m.submodules.r_port = r_port = storage.read_port(domain='comb')

        base = Signal(32)
        offset = Signal(8)

        with m.FSM() as fsm:

            m.d.comb += [
                self.bbus.blk_stall             .eq(~fsm.ongoing("IDLE")),
            ]

            with m.State("IDLE"):

                with m.If(self.bbus.blk & self.bbus.load):
                    m.next = "OP_BEGIN"
                    m.d.sync += [
                        base                    .eq(self.bbus.base),
                        offset                  .eq(0),
                    ]

            with m.State("OP_BEGIN"):
                m.d.comb += self.wbbus.cyc      .eq(1)
                m.d.comb += self.wbbus.stb      .eq(1)

                with m.If(~self.wbbus.stall):
                    m.next = "OP_WAIT"

            with m.State("OP_WAIT"):
                m.d.comb += self.wbbus.cyc      .eq(1)

                with m.If(self.wbbus.ack):

                    with m.If(self.bbus.blk & (offset != 127)):
                        m.next = "OP_BEGIN"
                        m.d.sync += offset      .eq(offset + 1)
                    with m.Else():
                        m.next = "IDLE"

        m.d.comb += [
            agen.base           .eq(base),
            agen.offset         .eq(offset),

            self.wbbus.sel      .eq(Value.cast(1).replicate(4)),
            self.wbbus.adr      .eq(agen.addr),

            w_port.addr         .eq(offset),
            w_port.data         .eq(self.wbbus.dat_r),
            w_port.en           .eq(self.wbbus.ack),

            r_port.addr         .eq(self.bbus.off),
        ]

        m.d.sync += [
            self.bbus.stall     .eq(0),
            self.bbus.ack       .eq(self.bbus.cyc & self.bbus.stb),
            self.bbus.dat_r     .eq(r_port.data),
        ]

        return m

    def ports(self):
        return [
            self.bbus,
            self.wbbus,
        ]
