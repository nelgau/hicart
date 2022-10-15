from amaranth import *
from amaranth_soc import wishbone
from lambdasoc.periph.sram  import SRAMPeripheral

import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
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

        # 30 == 32 - log_int (32 / granularity)
        self.bus = wishbone.Interface(addr_width=30, data_width=32, granularity=8, features={"cti", "bte", "err"}, name="bus")

        self.arbiter = wishbone.Arbiter(addr_width=30, data_width=32, granularity=8, features={"cti", "bte", "err"})
        self.decoder = wishbone.Decoder(addr_width=30, data_width=32, granularity=8, features={"cti", "bte", "err"})

        config = litesdcard.ECP5Config(clk_freq=int(80e6))
        self.litesdcard = litesdcard.Core(config, pins=self.pins)

        self.ram = SRAMPeripheral(size=0x100)

    def build(self, platform):
        build_dir = "build/cores"
        self.litesdcard.build(litesdcard.Builder(), platform, build_dir)

    def elaborate(self, platform):
        m = Module()

        m.submodules.arbiter = self.arbiter
        m.submodules.decoder = self.decoder
        m.submodules.litesdcard = self.litesdcard
        m.submodules.ram = self.ram

        self.arbiter.add(self.bus)
        self.arbiter.add(self.litesdcard.dma_bus)

        self.decoder.add(self.litesdcard.ctrl_bus, addr=0x00000)
        self.decoder.add(self.ram.bus, addr=0x10000)

        m.d.comb += [
            self.arbiter.bus.connect(self.decoder.bus),
        ]

        return m

    def ports(self):
        return [
            self.pins,
            self.bus,
        ]


@cocotb.test()
async def run_CocotbTest_test_module(dut):
    init_domains(dut)
    start_clock(dut.clk, rate=60e6)

    sd_card  = sd_card_accessor(dut, name="sd")
    bus = wishbone_accessor(dut, "bus", features={"cti", "bte", "err"})

    sd_card.cmd.i           .setimmediatevalue(0)
    sd_card.dat.i           .setimmediatevalue(0)
    sd_card.cd              .setimmediatevalue(0)

    # This shouldn't be necessary? I would expect that, after reset and at idle
    # the arbiter should hold this signal low. I need to examine the verilog.
    bus.err                 .setimmediatevalue(0)

    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0

    wb_master = WishboneMaster(
        dut,
        "bus",
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

    res = await wb_master.send_cycle([WBOp(0x0001)])

    for i in range(20):
        await FallingEdge(dut.clk)


class CocotbTest(CocotbTestCase):
    def test_module(self):
        platform = HomeInvaderRevAPlatform()

        dut = DUT()
        dut.build(platform)

        self.simulate(dut, traces=dut.ports(), platform=platform)
