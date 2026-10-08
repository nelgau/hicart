from amaranth import *
from amaranth.lib import crc, enum, stream, wiring
from amaranth.lib.wiring import In, Out


CRC7_SD_CMD  = crc.catalog.CRC7_MMC
CRC16_SD_DAT = crc.catalog.CRC16_XMODEM


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
    start: In(1)
    done: Out(1)

    sd_cmd_o: Out(1)
    sd_cmd_oe: Out(1)

    sd_clk_rising: In(1)
    sd_clk_falling: In(1)

    cmd_index: In(6)
    cmd_arg: In(32)

    def elaborate(self, platform):
        m = Module()

        out_shift = Signal(8, init=0xFF)

        byte_index = Signal(range(6))
        bit_index = Signal(range(8))
        bit_shifted = Signal()

        # Output

        m.d.comb += self.sd_cmd_o.eq(out_shift[7])

        # CRC

        crc7 = crc.catalog.CRC7_MMC(data_width=1).create()
        m.submodules.crc7 = crc7

        m.d.comb += crc7.data.eq(out_shift[7])
        m.d.comb += crc7.valid.eq(bit_shifted)

        # State machine

        m.d.sync += self.done.eq(0)
        m.d.sync += bit_shifted.eq(0)

        with m.FSM():

            with m.State("IDLE"):
                with m.If(self.start):
                    m.next = "WAIT_START"
                    m.d.comb += crc7.start.eq(1)

            with m.State("WAIT_START"):
                with m.If(self.sd_clk_falling):
                    m.next = "RUN"
                    m.d.sync += self.sd_cmd_oe.eq(1)
                    m.d.sync += out_shift.eq(Cat(self.cmd_index, C(1, 2))),
                    m.d.sync += bit_shifted.eq(1)

            with m.State("RUN"):
                with m.If(self.sd_clk_falling):
                    m.d.sync += bit_shifted.eq(1)

                    with m.If(bit_index == 7):
                        m.d.sync += bit_index.eq(0)
                        m.d.sync += byte_index.eq(byte_index + 1)

                        with m.If(byte_index == 5):
                            m.next = "IDLE"
                            m.d.sync += self.sd_cmd_oe.eq(0)
                            m.d.sync += byte_index.eq(0)
                            m.d.sync += self.done.eq(1)

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

                    with m.Else():
                        m.d.sync += out_shift.eq(Cat(0, out_shift[0:7]))
                        m.d.sync += bit_index.eq(bit_index + 1)

        return m


class CmdRx(wiring.Component):
    start: In(1)
    done: Out(1)

    sd_cmd_i: In(1)

    sd_clk_rising: In(1)
    sd_clk_falling: In(1)

    long_response: In(1)

    cmd_index: Out(6)
    cmd_resp: Out(128)

    dir_err: Out(1)
    crc_err: Out(1)
    end_err: Out(1)
    timeout: Out(1)

    def elaborate(self, platform):
        m = Module()

        in_shift = Signal(8)

        byte_index = Signal(range(17))
        bit_index = Signal(range(8))
        bit_shifted = Signal()
        crc_digesting = Signal()

        timeout_counter = Signal(range(64))

        # CRC

        crc7 = CRC7_SD_CMD(data_width=1).create()
        m.submodules.crc7 = crc7

        m.d.comb += crc7.data.eq(in_shift[0])
        m.d.comb += crc7.valid.eq(crc_digesting & bit_shifted)

        # State machine

        m.d.sync += self.done.eq(0)
        m.d.sync += bit_shifted.eq(0)

        with m.FSM():

            with m.State("IDLE"):
                with m.If(self.start):
                    m.next = "WAIT_START"
                    m.d.sync += self.cmd_index.eq(0)
                    m.d.sync += self.cmd_resp.eq(0)

                    m.d.sync += self.dir_err.eq(0)
                    m.d.sync += self.crc_err.eq(0)
                    m.d.sync += self.end_err.eq(0)
                    m.d.sync += self.timeout.eq(0)

                    m.d.sync += timeout_counter.eq(0)
                    m.d.comb += crc7.start.eq(1)

            with m.State("WAIT_START"):
                with m.If(self.sd_clk_rising):
                    m.d.sync += timeout_counter.eq(timeout_counter + 1)
                    with m.If(timeout_counter == 63):
                        m.next = "IDLE"
                        m.d.sync += self.done.eq(1)
                        m.d.sync += self.timeout.eq(1)

                    with m.Elif(~self.sd_cmd_i):
                        m.next = "RUN"
                        m.d.sync += in_shift.eq(Cat(self.sd_cmd_i, C(0, 7)))
                        m.d.sync += bit_shifted.eq(1)

                        with m.If(~self.long_response):
                            m.d.sync += crc_digesting.eq(1)

            with m.State("RUN"):
                with m.If(self.sd_clk_rising):
                    m.d.sync += in_shift.eq(Cat(self.sd_cmd_i, in_shift[:7]))
                    m.d.sync += bit_index.eq(bit_index + 1)
                    m.d.sync += bit_shifted.eq(1)

                    with m.If(bit_index == 7):
                        m.d.sync += bit_index.eq(0)
                        m.d.sync += byte_index.eq(byte_index + 1)

                        def finalize_first_byte():
                            with m.If(in_shift[6]):
                                m.d.sync += self.dir_err.eq(1)

                        def finalize_last_byte():
                            m.next = "IDLE"
                            m.d.sync += byte_index.eq(0)
                            m.d.sync += self.done.eq(1)

                            with m.If(in_shift[1:8] != crc7.crc):
                                m.d.sync += self.crc_err.eq(1)
                            with m.If(~in_shift[0]):
                                m.d.sync += self.end_err.eq(1)

                        def latch_resp_byte(index):
                            segment = slice(index * 8, (index + 1) * 8)
                            m.d.sync += self.cmd_resp[segment].eq(in_shift)

                        with m.If(self.long_response):

                            with m.Switch(byte_index):
                                with m.Case(0):
                                    m.d.sync += self.cmd_index.eq(in_shift[:6])
                                    m.d.sync += crc_digesting.eq(1)
                                    finalize_first_byte()
                                with m.Case(15):
                                    m.d.sync += crc_digesting.eq(0)
                                with m.Case(16):
                                    finalize_last_byte()

                            with m.Switch(byte_index):
                                for i in range(16):
                                    with m.Case(i + 1):
                                        latch_resp_byte(15 - i)

                        with m.Else():

                            with m.Switch(byte_index):
                                with m.Case(0):
                                    m.d.sync += self.cmd_index.eq(in_shift[:6])
                                    finalize_first_byte()
                                with m.Case(4):
                                    m.d.sync += crc_digesting.eq(0)
                                with m.Case(5):
                                    finalize_last_byte()

                            with m.Switch(byte_index):
                                for i in range(4):
                                    with m.Case(i + 1):
                                        latch_resp_byte(3 - i)

        return m


class CmdUnit(wiring.Component):
    start: In(1)
    done: Out(1)

    sd_cmd_i: In(1)
    sd_cmd_o: Out(1)
    sd_cmd_oe: Out(1)
    sd_dat0_i: In(1)

    sd_clk_rising: In(1)
    sd_clk_falling: In(1)

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

        # RX

        cmd_rx = CmdRx()
        m.submodules.cmd_rx = cmd_rx

        m.d.comb += [
            cmd_rx.sd_cmd_i         .eq(self.sd_cmd_i),

            cmd_rx.sd_clk_rising    .eq(self.sd_clk_rising),
            cmd_rx.sd_clk_falling   .eq(self.sd_clk_falling),

            cmd_rx.long_response    .eq(self.long_response),

            self.cmd_resp           .eq(cmd_rx.cmd_resp),
        ]

        # State machine

        m.d.sync += self.done.eq(0)
        m.d.sync += cmd_tx.start.eq(0)
        m.d.sync += cmd_rx.start.eq(0)

        with m.FSM():

            with m.State("IDLE"):
                with m.If(self.start):
                    m.next = "TX"
                    m.d.sync += cmd_tx.start.eq(1)

            with m.State("TX"):
                with m.If(cmd_tx.done):
                    with m.If(self.has_response):
                        m.next = "RX"
                        m.d.sync += cmd_rx.start.eq(1)
                    with m.Elif(self.wait_not_busy):
                        m.next = "WAIT_NOT_BUSY"
                    with m.Else():
                        m.next = "IDLE"
                        m.d.sync += self.done.eq(1)

            with m.State("RX"):
                with m.If(cmd_rx.done):
                    with m.If(self.wait_not_busy):
                        m.next = "WAIT_NOT_BUSY"
                    with m.Else():
                        m.next = "IDLE"
                        m.d.sync += self.done.eq(1)

            with m.State("WAIT_NOT_BUSY"):
                with m.If(self.sd_clk_rising):
                    with m.If(self.sd_dat0_i):
                        m.next = "IDLE"
                        m.d.sync += self.done.eq(1)

        return m


class DatRx(wiring.Component):
    start: In(1)
    done: Out(1)

    sd_dat_i: In(4)

    sd_clk_rising: In(1)
    sd_clk_falling: In(1)

    block_length: In(10)
    block_count: In(8)

    source: Out(stream.Signature(8, always_ready=True))

    crc_err: Out(1)
    end_err: Out(1)
    timeout: Out(1)

    def elaborate(self, platform):
        m = Module()

        in_shift = Signal(8)

        block_index = Signal(8)
        byte_index = Signal(10)
        nibble_index = Signal(range(2))

        crc_start = Signal()
        crc_digest = Signal()
        crc_finalize = Signal()
        crc_index = Signal(range(16))
        crc_shifts = [Signal(16, name=f"crc_shift_{i}") for i in range(4)]

        timeout_counter = Signal()

        # Output

        m.d.comb += self.source.payload.eq(in_shift)

        # CRC

        crc_units = []
        for i in range(4):
            crc_unit = CRC16_SD_DAT(data_width=1).create()
            crc_units.append(crc_unit)

            m.submodules[f"crc_{i}"] = crc_unit

            m.d.comb += crc_unit.start.eq(crc_start)
            m.d.comb += crc_unit.valid.eq(crc_digest)
            m.d.comb += crc_unit.data.eq(self.sd_dat_i[i])

            with m.If(crc_finalize):
                m.d.sync += crc_shifts[i].eq(crc_units[i].crc)

        # State machine

        m.d.sync += self.done.eq(0)
        m.d.sync += self.source.valid.eq(0)
        m.d.sync += crc_finalize.eq(0)

        with m.FSM():

            with m.State("IDLE"):
                with m.If(self.start):
                    m.next = "WAIT_START"
                    m.d.sync += self.crc_err.eq(0)
                    m.d.sync += self.end_err.eq(0)
                    m.d.sync += self.timeout.eq(0)

                    m.d.sync += block_index.eq(0)
                    m.d.sync += byte_index.eq(0)
                    m.d.sync += nibble_index.eq(0)

                    m.d.sync += timeout_counter.eq(0)

            with m.State("WAIT_START"):
                with m.If(self.sd_clk_rising):
                    # Handle timeout

                    with m.If(~self.sd_dat_i):
                        m.next = "DATA"
                        m.d.sync += timeout_counter.eq(0)
                        m.d.comb += crc_start.eq(1)

            with m.State("DATA"):
                with m.If(self.sd_clk_rising):
                    m.d.sync += in_shift.eq(Cat(self.sd_dat_i, in_shift[:4]))
                    m.d.sync += nibble_index.eq(nibble_index + 1)
                    m.d.comb += crc_digest.eq(1)

                    with m.If(nibble_index == 1):
                        m.d.sync += nibble_index.eq(0)
                        m.d.sync += byte_index.eq(byte_index + 1)
                        m.d.sync += self.source.valid.eq(1)

                        with m.If(byte_index == self.block_length - 1):
                            m.next = "CRC"
                            m.d.sync += crc_index.eq(0)
                            m.d.sync += crc_finalize.eq(1)

            with m.State("CRC"):
                with m.If(self.sd_clk_rising):
                    m.d.sync += crc_index.eq(crc_index + 1)

                    for i in range(4):
                        m.d.sync += crc_shifts[i].eq(Cat(C(0), crc_shifts[i][:15]))

                        with m.If(self.sd_dat_i[i] != crc_shifts[i][15]):
                            m.d.sync += self.crc_err.eq(1)

                    with m.If(crc_index == 15):
                        m.next = "END"

            with m.State("END"):
                with m.If(self.sd_clk_rising):
                    m.d.sync += block_index.eq(block_index + 1)

                    with m.If(~self.sd_dat_i):
                        m.d.sync += self.end_err.eq(1)

                    with m.If(block_index == self.block_count - 1):
                        m.next = "IDLE"
                        m.d.sync += self.done.eq(1)
                    with m.Else():
                        m.next = "WAIT_START"
                        m.d.sync += byte_index.eq(0)

        return m


class SDController(wiring.Component):
    bus: Out(SDBusSignature())

    start: In(1)
    done: Out(1)
    ready: Out(1)

    cmd_index: In(6)
    cmd_arg: In(32)
    cmd_resp: Out(128)

    has_response: In(1)
    long_response: In(1)
    wait_not_busy: In(1)

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

        # Command unit

        cmd_unit = CmdUnit()
        m.submodules.cmd_unit = cmd_unit

        m.d.comb += [
            cmd_unit.sd_cmd_i       .eq(self.bus.cmd.i),
            self.bus.cmd.o          .eq(cmd_unit.sd_cmd_o),
            self.bus.cmd.oe         .eq(cmd_unit.sd_cmd_oe),
            cmd_unit.sd_dat0_i      .eq(self.bus.dat.i[0]),

            cmd_unit.sd_clk_rising  .eq(clocker.sd_clk_rising),
            cmd_unit.sd_clk_falling .eq(clocker.sd_clk_falling),

            cmd_unit.cmd_index      .eq(self.cmd_index),
            cmd_unit.cmd_arg        .eq(self.cmd_arg),
            self.cmd_resp           .eq(cmd_unit.cmd_resp),

            cmd_unit.has_response   .eq(self.has_response),
            cmd_unit.long_response  .eq(self.long_response),
            cmd_unit.wait_not_busy  .eq(self.wait_not_busy),
        ]

        # State machine

        counter = Signal(20)

        m.d.sync += self.done.eq(0)
        m.d.sync += cmd_unit.start.eq(0)

        with m.FSM() as fsm:
            m.d.comb += self.ready.eq(fsm.ongoing("IDLE"))

            with m.State("INIT"):
                m.d.sync += counter.eq(counter + 1)
                with m.If(counter == self._startup_delay):
                    m.next = "IDLE"

            with m.State("IDLE"):
                with m.If(self.start):
                    m.next = "RUN"
                    m.d.sync += cmd_unit.start.eq(1)

            with m.State("RUN"):
                with m.If(cmd_unit.done):
                    m.next = "WAIT"
                    m.d.sync += counter.eq(0)

            with m.State("WAIT"):
                with m.If(clocker.sd_clk_rising):
                    m.d.sync += counter.eq(counter + 1)

                with m.If(counter == 8):
                    m.next = "IDLE"
                    m.d.sync += self.done.eq(1)

        return m


class SDSequencer(Elaboratable):

    def __init__(self, *, ctrlr):
        self.ctrlr = ctrlr

    def elaborate(self, platform):
        m = Module()

        step_index = Signal(8)
        rca = Signal(16)

        # Sequence

        def load_signals():
            with m.Switch(step_index):

                with m.Case(0):
                    m.d.sync += [
                        self.ctrlr.cmd_index        .eq(0),
                        self.ctrlr.cmd_arg          .eq(0),
                        self.ctrlr.has_response     .eq(0),
                        self.ctrlr.long_response    .eq(0),
                        self.ctrlr.wait_not_busy    .eq(0),
                    ]

                with m.Case(1):
                    m.d.sync += [
                        self.ctrlr.cmd_index        .eq(8),
                        self.ctrlr.cmd_arg          .eq(0x000001AA),
                        self.ctrlr.has_response     .eq(1),
                        self.ctrlr.long_response    .eq(0),
                        self.ctrlr.wait_not_busy    .eq(0),
                    ]

                with m.Case(2):
                    m.d.sync += [
                        self.ctrlr.cmd_index        .eq(55),
                        self.ctrlr.cmd_arg          .eq(0),
                        self.ctrlr.has_response     .eq(1),
                        self.ctrlr.long_response    .eq(0),
                        self.ctrlr.wait_not_busy    .eq(0),
                    ]

                with m.Case(3):
                    m.d.sync += [
                        self.ctrlr.cmd_index        .eq(41),
                        self.ctrlr.cmd_arg          .eq(0x40ff8000),
                        self.ctrlr.has_response     .eq(1),
                        self.ctrlr.long_response    .eq(0),
                        self.ctrlr.wait_not_busy    .eq(0),
                    ]

                with m.Case(4):
                    m.d.sync += [
                        self.ctrlr.cmd_index        .eq(2),
                        self.ctrlr.cmd_arg          .eq(0),
                        self.ctrlr.has_response     .eq(1),
                        self.ctrlr.long_response    .eq(1),
                        self.ctrlr.wait_not_busy    .eq(0),
                    ]

                with m.Case(5):
                    m.d.sync += [
                        self.ctrlr.cmd_index        .eq(3),
                        self.ctrlr.cmd_arg          .eq(0),
                        self.ctrlr.has_response     .eq(1),
                        self.ctrlr.long_response    .eq(0),
                        self.ctrlr.wait_not_busy    .eq(0),
                    ]

                with m.Case(6):
                    m.d.sync += [
                        self.ctrlr.cmd_index        .eq(7),
                        self.ctrlr.cmd_arg          .eq(rca << 16),
                        self.ctrlr.has_response     .eq(1),
                        self.ctrlr.long_response    .eq(0),
                        self.ctrlr.wait_not_busy    .eq(1),
                    ]

                with m.Case(7):
                    m.d.sync += [
                        self.ctrlr.cmd_index        .eq(55),
                        self.ctrlr.cmd_arg          .eq(rca << 16),
                        self.ctrlr.has_response     .eq(1),
                        self.ctrlr.long_response    .eq(0),
                        self.ctrlr.wait_not_busy    .eq(0),
                    ]

                with m.Case(8):
                    m.d.sync += [
                        self.ctrlr.cmd_index        .eq(6),
                        self.ctrlr.cmd_arg          .eq(0x00000002),
                        self.ctrlr.has_response     .eq(1),
                        self.ctrlr.long_response    .eq(0),
                        self.ctrlr.wait_not_busy    .eq(1),
                    ]

                with m.Case(9):
                    m.d.sync += [
                        self.ctrlr.cmd_index        .eq(17),
                        self.ctrlr.cmd_arg          .eq(0x00000000),
                        self.ctrlr.has_response     .eq(1),
                        self.ctrlr.long_response    .eq(0),
                        self.ctrlr.wait_not_busy    .eq(0),
                    ]

                with m.Default():
                    m.next = "DONE"

        def process_result():
            with m.Switch(step_index):

                with m.Case(3):
                    with m.If(~self.ctrlr.cmd_resp[31]):
                        m.d.sync += step_index.eq(2)

                with m.Case(5):
                    m.d.sync += rca.eq(self.ctrlr.cmd_resp[16:32])

        # State machine

        with m.FSM():

            with m.State("IDLE"):
                m.next = "LOAD"

            with m.State("LOAD"):
                m.next = "START"
                load_signals()

            with m.State("START"):
                m.next = "WAIT_RUN"
                m.d.sync += self.ctrlr.start.eq(1)

            with m.State("WAIT_RUN"):
                with m.If(self.ctrlr.ready):
                    m.next = "WAIT_DONE"
                    m.d.sync += self.ctrlr.start.eq(0)

            with m.State("WAIT_DONE"):
                with m.If(self.ctrlr.done):
                    m.next = "LOAD"
                    m.d.sync += step_index.eq(step_index + 1)
                    process_result()

            with m.State("DONE"):
                pass

        return m
