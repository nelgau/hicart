from amaranth import *
from amaranth.sim import *
from amaranth_soc import wishbone

from hicart.interface.qspi_flash import QSPIBus, QSPIFlashWishboneInterface
from hicart.n64.ad16 import AD16
from hicart.n64.pi import PIWishboneInitiator
from hicart.soc.wishbone import DownConverter, Translator

from hicart.test.cocotb_harness import run, get_current_module

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge


class DUT(Elaboratable):

    def __init__(self):
        self.ad16 = AD16()
        self.qspi = QSPIBus()

        self.flash_interface = QSPIFlashWishboneInterface()

        self.translator = Translator(sub_bus=self.flash_interface.bus,
                                        base_addr=0x800000,
                                        addr_width=24,
                                        features={"stall"})

        self.down_converter = DownConverter(sub_bus=self.translator.bus,
                                        addr_width=22,
                                        data_width=32,
                                        granularity=8,
                                        features={"stall"})

    def elaborate(self, platform):
        m = Module()

        initiator = PIWishboneInitiator()
        
        decoder = wishbone.Decoder(addr_width=32, data_width=32, granularity=8, features={"stall"})
        decoder.add(self.down_converter.bus, addr=0x10000000)

        m.submodules.initiator       = initiator
        m.submodules.decoder         = decoder
        m.submodules.flash_interface = self.flash_interface
        m.submodules.translator      = self.translator
        m.submodules.down_converter  = self.down_converter

        m.d.comb += [
            initiator.ad16              .connect( self.ad16 ),
            initiator.bus               .connect( decoder.bus ),
            self.flash_interface.qspi   .connect( self.qspi ),
        ]

        return m

    def ports(self):
        return [
            self.ad16.ad.i,
            self.ad16.ad.o,
            self.ad16.ad.oe,
            self.ad16.ale_h,
            self.ad16.ale_l,
            self.ad16.read,
            self.ad16.write,
            self.ad16.reset,

            self.qspi.sck,
            self.qspi.cs_n,
            self.qspi.d.i,
            self.qspi.d.o,
            self.qspi.d.oe,
        ]


@cocotb.test()
async def run_test_module(dut):
    dut.ad__i.value = 0
    dut.ale_h.value = 0
    dut.ale_l.value = 0
    dut.clk.value = 0
    dut.d__i.value = 0

    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    for i in range(20):
        await FallingEdge(dut.clk)
    

def test_module():
    dut = DUT()
    run(
        dut,

        # It isn't possible to use this 
        # get_current_module()
        'tests.test_cocotb',

        ports=dut.ports(),
        vcd_file='output.vcd'
    )


if __name__ == '__main__':
    test_module()
