from amaranth import *
from amaranth_soc import wishbone
import cocotb
from cocotb.triggers import FallingEdge
from cocotbext.wishbone.driver import WishboneMaster
from cocotbext.wishbone.driver import WBOp

from hicart.cores import litesdcard
from hicart.platforms.homeinvader_rev_a import HomeInvaderRevAPlatform
from hicart.test.cocotb import CocotbTestCase, init_domains, start_clock
from hicart.test.cocotb.accessor import wishbone_accessor, Accessor


sd_card_accessor = Accessor.from_layout(litesdcard.sd_card_layout)


class DUT(Elaboratable):
    def __init__(self):
        self.pins = litesdcard.SDCard(name="sd")

        self.ctrl_bus = wishbone.Interface(
            addr_width=30,      # 32 - log_int (32 / granularity)
            data_width=32,
            granularity=8,
            features={"cti", "bte", "err"}
        )

        self.dma_bus = wishbone.Interface(
            addr_width=30,      # 32 - log_int (32 / granularity)
            data_width=32,
            granularity=8,
            features={"cti", "bte", "err"}
        )

        config = litesdcard.ECP5Config(clk_freq=int(80e6))
        self.litesdcard = litesdcard.Core(config, pins=self.pins)

    def build(self, platform):
        build_dir = "build/cores"
        self.litesdcard.build(litesdcard.Builder(), platform, build_dir)

    def elaborate(self, platform):
        m = Module()

        m.submodules.litesdcard = self.litesdcard

        m.d.comb += [
            self.ctrl_bus               .connect( self.litesdcard.ctrl_bus ),
            self.litesdcard.dma_bus     .connect (self.dma_bus )
        ]

        return m

    def ports(self):
        return [
            self.pins,
            self.ctrl_bus,
            self.dma_bus,
        ]


@cocotb.test()
async def run_CocotbTest_test_module(dut):
    ctrl_bus = wishbone_accessor(dut, name="ctrl_bus", features={"cti", "bte", "err"})
    dma_bus  = wishbone_accessor(dut, name="dma_bus",  features={"cti", "bte", "err"})
    sd_card  = sd_card_accessor(dut, name="sd")

    init_domains(dut)
    start_clock(dut.clk, rate=60e6)

    dma_bus.dat_r           .setimmediatevalue(0)
    dma_bus.ack             .setimmediatevalue(0)
    dma_bus.err             .setimmediatevalue(0)

    sd_card.cmd.i           .setimmediatevalue(0)
    sd_card.dat.i           .setimmediatevalue(0)
    sd_card.cd              .setimmediatevalue(0)

    wb_master = WishboneMaster(
        dut,
        "ctrl_bus",
        dut.clk,
        timeout=10,
        bus_separator="__",
        signals_dict={
            "adr": "adr",
            "datrd": "dat_r",
            "datwr": "dat_w",
            "cyc": "cyc",
            "stb": "stb",
            "sel": "sel",
            "we": "we",
            "ack": "ack",
            "cti": "cti",
            "bte": "bte",
            "err": "err",
        })

    await FallingEdge(dut.clk)

    res = await wb_master.send_cycle([WBOp(0x4000)])

    for i in range(20):
        await FallingEdge(dut.clk)


class CocotbTest(CocotbTestCase):
    def test_module(self):
        platform = HomeInvaderRevAPlatform()

        dut = DUT()
        dut.build(platform)

        self.simulate(dut, traces=dut.ports(), platform=platform)
