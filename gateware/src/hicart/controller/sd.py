from amaranth import *
from amaranth.lib import data, enum, wiring
from amaranth.lib.wiring import In, Out


class SBBusSignature(wiring.Signature):
    def __init__(self):
        super().__init__({
            "clk":  Out(1),
            "cmd":  Out(1),
            "dat":  Out(wiring.Signature({
                "i":    In(4),
                "o":    Out(4),
                "oe":   Out(4),
            })),
            "card_present": In(1),
        })


class RespType(enum.Enum, shape=3):
    NONE = 0
    R1   = 1   # 48-bit, CRC7 + index check (also R6, R7)
    R1B  = 2   # R1, then wait for busy release on DAT0
    R2   = 3   # 136-bit (CID, CSD)
    R3   = 4   # 48-bit, no CRC, no index check (OCR)


class DataDir(enum.Enum, shape=2):
    NONE  = 0
    READ  = 1  # card -> buffer
    WRITE = 2  # buffer -> card


class DataDest(enum.Enum, shape=1):
    SECTOR = 0
    AUX    = 1


class Status(enum.Enum, shape=3):
    OK           = 0
    CMD_TIMEOUT  = 1   # card never answered on CMD
    CMD_BAD      = 2   # answered, but CRC/index/end bit wrong
    DATA_TIMEOUT = 3   # DAT never started, or busy never released
    DATA_CRC     = 4   # a block's CRC16 failed


class Descriptor(data.Struct):
    cmd_index:   6
    cmd_arg:     32
    resp_type:   RespType
    data_dir:    DataDir
    data_dest:   DataDest
    buf_addr:    16    # byte offset
    block_len:   10    # bytes per block, up to 512
    block_count: 16


class Config(data.Struct):
    clk_div:     8    # SD CLK = sys_clk / (2 * (clk_div + 1))
    bus_width_4: 1
    timeout:     24   # in SD clocks


class ControlSignature(wiring.Signature):
    def __init__(self):
        super().__init__({
            "desc":   Out(Descriptor),
            "config": Out(Config),
            "start":  Out(1),
            "busy":   In(1),
            "done":   In(1),
            "resp":   In(128),
            "status": In(Status),
        })


