from amaranth import *
from amaranth_soc import wishbone
import cocotb
from cocotb.triggers import FallingEdge

from hicart.cores import litesdcard
from hicart.platforms.homeinvader_rev_a import HomeInvaderRevAPlatform
from hicart.test.cocotb import CocotbTestCase, init_domains, start_clock


class DUT(Elaboratable):
    def __init__(self):
        self.pins = litesdcard.SDCard()
    
        config = litesdcard.ECP5Config(clk_freq=int(80e6))
        self.litesdcard = litesdcard.Core(config, pins=self.pins)

    def build(self, platform):
        build_dir = "build/cores"
        self.litesdcard.build(litesdcard.Builder(), platform, build_dir)

    def elaborate(self, platform):
        m = Module()
        m.submodules.litesdcard = self.litesdcard
        return m

    def ports(self):
        return [
            self.litesdcard._pins,
            self.litesdcard.ctrl_bus,
            self.litesdcard.dma_bus
        ]


@cocotb.test()
async def run_CocotbTest_test_module(dut):
    init_domains(dut)
    start_clock(dut.clk, rate=60e6)

    dut._ctrl_bus__adr      .setimmediatevalue(0)
    dut._ctrl_bus__dat_w    .setimmediatevalue(0)
    dut._ctrl_bus__sel      .setimmediatevalue(0)
    dut._ctrl_bus__cyc      .setimmediatevalue(0)
    dut._ctrl_bus__stb      .setimmediatevalue(0)
    dut._ctrl_bus__we       .setimmediatevalue(0)
    dut._ctrl_bus__cti      .setimmediatevalue(0)
    dut._ctrl_bus__bte      .setimmediatevalue(0)
    dut._dma_bus__dat_r     .setimmediatevalue(0)
    dut._dma_bus__ack       .setimmediatevalue(0)
    dut._dma_bus__err       .setimmediatevalue(0)
    dut.cmd__i              .setimmediatevalue(0)
    dut.dat__i              .setimmediatevalue(0)
    dut.cd                  .setimmediatevalue(0)

    # for i in range(20):
    #     await FallingEdge(dut.clk)

class CocotbTest(CocotbTestCase):
    def test_module(self):
        platform = HomeInvaderRevAPlatform()

        dut = DUT()
        dut.build(platform)

        self.simulate(dut, traces=dut.ports(), platform=platform)
