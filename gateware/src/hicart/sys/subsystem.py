from amaranth import *
from amaranth.lib import cdc, wiring
from amaranth.lib.wiring import In, Out, flipped

from hicart.controller import sd
from hicart.n64.cart import CICSignature, CtlSignature
from hicart.soc.cpu_block import CpuBlock, CpuBlockConfig
from hicart.sys.cic import CIC
from hicart.sys.sd import SDBufferWriter


class SysSubsystem(wiring.Component):
    cart_cic: Out(CICSignature)
    cart_ctl: Out(CtlSignature)

    sd_bus: Out(sd.BusSignature())

    def __init__(self, *, crossing):
        self.crossing = crossing
        super().__init__()

        # self.mcu = MCU(mailbox_bus=crossing.mailbox.sys_bus)

        mcu_config = CpuBlockConfig(rom_size=0x1000, ram_size=0x1000)
        mcu_config.add_csr(crossing.mailbox.sys_bus, name="mailbox", addr=0xC000_0000)

        self.mcu = CpuBlock(mcu_config)

        for ri in self.mcu.memory_map.all_resources():
            print(ri.path, hex(ri.start), hex(ri.end))

        self.cic = CIC()

        sd_config = sd.ControllerConfig(clk_freq=40e6)
        self.sd_periph = sd.Peripheral(config=sd_config)

        self.writer = SDBufferWriter(writer_bus=crossing.sd_buffer.writer_bus)

    def elaborate(self, platform):
        m = Module()

        # MCU

        m.submodules.mcu = self.mcu

        with open("../firmware/mcu/build/mcu.bin", "rb") as f:
            self.mcu.firmware = f.read()

        # CIC

        m.submodules.cic = self.cic
        m.submodules += cdc.AsyncFFSynchronizer(self.cart_ctl.reset, self.cic.reset)

        wiring.connect(m, self.cic.bus, flipped(self.cart_cic))

        # SD Controller

        m.submodules.sd_periph = self.sd_periph
        m.submodules.writer = self.writer

        wiring.connect(m, self.sd_periph.sd_bus, flipped(self.sd_bus))

        wiring.connect(m, self.sd_periph.source, self.writer.sink)
        wiring.connect(m, self.writer.writer_bus, self.crossing.sd_buffer.writer_bus)

        return m
