from amaranth import *
from amaranth.lib import crc, enum, wiring
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


class CmdType(enum.Enum, shape=2):
    RESPONSE_NONE = 0
    RESPONSE_SHORT = 1
    RESPONSE_LONG = 2
    RESPONSE_SHORT_BUSY = 3


class Clocker(wiring.Component):
    enable: In(1)
    divisor: In(10)

    sd_clk: Out(1)
    sd_clk_rising: Out(1)
    sd_clk_falling: Out(1)

    def elaborate(self, platform):
        m = Module()

        counter = Signal(10)

        with m.If(self.enable):
            with m.If(counter <= 1):
                m.d.sync += self.sd_clk.eq(~self.sd_clk)
                m.d.sync += counter.eq(self.divisor)

                m.d.comb += self.sd_clk_rising.eq(~self.sd_clk)
                m.d.comb += self.sd_clk_falling.eq(self.sd_clk)
            with m.Else():
                m.d.sync += counter.eq(counter - 1)

        return m


class CmdTx(wiring.Component):
    sd_cmd_o: Out(1)
    sd_cmd_oe: Out(1)

    sd_clk_rising: In(1)
    sd_clk_falling: In(1)

    start: In(1)
    busy: Out(1)
    done: Out(1)

    cmd_index: In(6)
    cmd_arg: In(32)

    def elaborate(self, platform):
        m = Module()

        out_shift = Signal(8, init=0xFF)
        byte_index = Signal(range(6))
        bit_index = Signal(range(8))

        # CRC

        crc7 = crc.catalog.CRC7_MMC(data_width=1).create()
        m.submodules.crc7 = crc7

        m.d.comb += crc7.data.eq(out_shift[7])

        # State machine

        m.d.sync += crc7.valid.eq(0)
        m.d.sync += self.done.eq(0)

        with m.FSM() as fsm:
            m.d.comb += self.busy.eq(~fsm.ongoing("IDLE"))

            with m.State("IDLE"):
                with m.If(self.start):
                    m.next = "WAIT_FALLING"

            with m.State("WAIT_FALLING"):
                with m.If(self.sd_clk_falling):
                    m.next = "RUN"
                    m.d.sync += out_shift.eq(Cat(self.cmd_index, Const(1, 2))),
                    m.d.sync += self.sd_cmd_oe.eq(1)
                    m.d.comb += crc7.start.eq(1)

            with m.State("RUN"):
                with m.If(self.sd_clk_falling):
                    m.d.sync += crc7.valid.eq(1)

                    with m.If(bit_index == 7):
                        m.d.sync += bit_index.eq(0)
                        m.d.sync += byte_index.eq(byte_index + 1)

                        with m.Switch(byte_index):
                            with m.Case(0):
                                m.d.sync += out_shift.eq(self.cmd_arg[24:32])
                            with m.Case(1):
                                m.d.sync += out_shift.eq(self.cmd_arg[16:24])
                            with m.Case(2):
                                m.d.sync += out_shift.eq(self.cmd_arg[8:16])
                            with m.Case(3):
                                m.d.sync += out_shift.eq(self.cmd_arg[0:8])
                            with m.Case(4):
                                m.d.sync += out_shift.eq(Cat(1, crc7.crc))

                            with m.Default():
                                m.next = "IDLE"
                                m.d.sync += self.sd_cmd_oe.eq(0)
                                m.d.sync += byte_index.eq(0)
                                m.d.sync += self.done.eq(1)

                    with m.Else():
                        m.d.sync += out_shift.eq(Cat(0, out_shift[0:7]))
                        m.d.sync += bit_index.eq(bit_index + 1)

        # Output

        m.d.comb += self.sd_cmd_o.eq(out_shift[7])

        return m


class CmdUnit(wiring.Component):
    sd_cmd_i: In(1)
    sd_cmd_o: Out(1)
    sd_cmd_oe: Out(1)

    sd_clk_rising: In(1)
    sd_clk_falling: In(1)

    start: In(1)
    busy: Out(1)
    done: Out(1)

    cmd_index: In(6)
    cmd_arg: In(32)
    cmd_resp: Out(128)

    has_response: In(1)
    long_response: In(1)
    wait_not_busy: In(1)

    def elaborate(self, platform):
        m = Module()

        # TX

        cmd_tx = CmdTx()
        m.submodules.cmd_tx = cmd_tx

        m.d.comb += [
            self.sd_cmd_o           .eq(cmd_tx.sd_cmd_o),
            self.sd_cmd_oe          .eq(cmd_tx.sd_cmd_oe),

            cmd_tx.sd_clk_rising    .eq(self.sd_clk_rising),
            cmd_tx.sd_clk_falling   .eq(self.sd_clk_falling),

            cmd_tx.cmd_index        .eq(self.cmd_index),
            cmd_tx.cmd_arg          .eq(self.cmd_arg),
        ]

        # State machine

        m.d.sync += [
            self.done.eq(0),
            cmd_tx.start.eq(0),
        ]

        with m.FSM() as fsm:
            m.d.comb += self.busy.eq(~fsm.ongoing("IDLE"))

            with m.State("IDLE"):
                with m.If(self.start):
                    m.next = "TX"
                    m.d.sync += cmd_tx.start.eq(1)

            with m.State("TX"):
                with m.If(cmd_tx.done):
                    m.next = "IDLE"
                    m.d.sync += self.done.eq(1)

        return m


class SDController(wiring.Component):
    bus: Out(SDBusSignature())

    def __init__(self, *, divisor=2, startup_delay=10):
        self._divisor = divisor
        self._startup_delay = startup_delay
        super().__init__()

    def elaborate(self, platform):
        m = Module()

        # Clocker

        clocker = Clocker()
        m.submodules.clocker = clocker

        m.d.comb += [
            self.bus.clk            .eq(clocker.sd_clk),

            clocker.enable          .eq(1),
            clocker.divisor         .eq(self._divisor),
        ]

        # Command TX

        cmd_unit = CmdUnit()
        m.submodules.cmd_unit = cmd_unit

        m.d.comb += [
            cmd_unit.sd_cmd_i       .eq(self.bus.cmd.i),
            self.bus.cmd.o          .eq(cmd_unit.sd_cmd_o),
            self.bus.cmd.oe         .eq(cmd_unit.sd_cmd_oe),

            cmd_unit.sd_clk_rising  .eq(clocker.sd_clk_rising),
            cmd_unit.sd_clk_falling .eq(clocker.sd_clk_falling),
        ]

        # State machine

        counter = Signal(20)
        step_index = Signal(4)

        m.d.sync += cmd_unit.start.eq(0)

        with m.FSM():

            with m.State("IDLE"):
                m.d.sync += counter.eq(counter + 1)
                with m.If(counter == self._startup_delay):
                    m.next = "STEP"

            with m.State("STEP"):
                with m.Switch(step_index):

                    with m.Case(0):
                        m.next = "WAIT"
                        m.d.sync += [
                            cmd_unit.cmd_index          .eq(0),
                            cmd_unit.cmd_arg            .eq(0),
                            cmd_unit.has_response       .eq(0),
                            cmd_unit.long_response      .eq(0),
                            cmd_unit.wait_not_busy      .eq(0),

                            cmd_unit.start              .eq(1),
                        ]

                    with m.Case(1):
                        m.next = "WAIT"
                        m.d.sync += [
                            cmd_unit.cmd_index          .eq(8),
                            cmd_unit.cmd_arg            .eq(0x000001AA),
                            cmd_unit.has_response       .eq(1),
                            cmd_unit.long_response      .eq(0),
                            cmd_unit.wait_not_busy      .eq(0),

                            cmd_unit.start              .eq(1),
                        ]

                    with m.Default():
                        m.next = "DONE"

            with m.State("WAIT"):
                with m.If(cmd_unit.done):
                    m.next = "WAIT_CLK"
                    m.d.sync += counter.eq(0)

            with m.State("WAIT_CLK"):
                with m.If(clocker.sd_clk_rising):
                    m.d.sync += counter.eq(counter + 1)

                with m.If(counter == 8):
                    m.next = "STEP"
                    m.d.sync += step_index.eq(step_index + 1)

            with m.State("DONE"):
                pass

        return m
