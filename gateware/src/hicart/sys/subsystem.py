from amaranth import *
from amaranth.lib import cdc, wiring
from amaranth.lib.wiring import In, Out, flipped

from hicart.controller import sd
from hicart.n64.cart import CICSignature, CtlSignature
from hicart.soc.cpu_block import CpuBlock, CpuBlockConfig
from hicart.sys.sd_buffer import SDBufferWriter
from hicart.sys.cic import CIC


class SysSubsystem(wiring.Component):
    cart_cic: Out(CICSignature)
    cart_ctl: Out(CtlSignature)

    sd_bus: Out(sd.BusSignature())

    def __init__(self, *, crossing):
        self.crossing = crossing
        super().__init__()

        # CIC

        self.cic = CIC()

        # SD

        sd_config = sd.ControllerConfig(clk_freq=40e6)
        self.sd_periph = sd.Peripheral(config=sd_config)
        self.sd_writer = SDBufferWriter(writer_bus=crossing.sd_buffer.writer_bus)

        # MCU

        mcu_config = CpuBlockConfig(rom_size=0x1000, ram_size=0x1000)
        mcu_config.add_csr(crossing.mailbox.sys_bus, name="mailbox", addr=0xC000_0000)
        mcu_config.add_csr(self.sd_periph.csr_bus, name="sd", addr=0xC000_0100)
        mcu_config.add_csr(self.sd_writer.csr_bus, name="sd_writer", addr=0xC000_0200)

        self.mcu = CpuBlock(mcu_config)

    def elaborate(self, platform):
        m = Module()

        # CIC

        m.submodules.cic = self.cic
        m.submodules += cdc.AsyncFFSynchronizer(self.cart_ctl.reset, self.cic.reset)

        wiring.connect(m, self.cic.bus, flipped(self.cart_cic))

        # SD Controller

        m.submodules.sd_periph = self.sd_periph
        m.submodules.sd_writer = self.sd_writer

        wiring.connect(m, self.sd_periph.sd_bus, flipped(self.sd_bus))

        wiring.connect(m, self.sd_periph.source, self.sd_writer.sink)
        wiring.connect(m, self.sd_writer.writer_bus, self.crossing.sd_buffer.writer_bus)

        # MCU

        m.submodules.mcu = self.mcu

        with open("../firmware/mcu/build/mcu.bin", "rb") as f:
            self.mcu.firmware = f.read()

        return m
