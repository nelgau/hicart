import argparse

from migen import *

from litex.build.io import SDROutput, SDRTristate
from litex.build.generic_platform import *
from litex.build.xilinx.platform import XilinxPlatform
from litex.build.altera.platform import AlteraPlatform
from litex.build.lattice.platform import LatticePlatform

from litex.soc.interconnect import wishbone
from litex.soc.interconnect.csr_eventmanager import *
from litex.soc.integration.soc import SoCBusHandler, SoCRegion
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *

from litesdcard.emulator import SDEmulator
from litesdcard.core import SDCore
from litesdcard.frontend.dma import SDBlock2MemDMA, SDMem2BlockDMA
from litesdcard.phy import SDPHYClocker, SDPHYInit
from litesdcard.phy import SDPHYCMDW, SDPHYCMDR, SDPHYDATAW, SDPHYDATAR, SDPHYIO


_sdpads_layout = [
    ("clk", 1),
    ("cmd", [
        ("i",  1),
        ("o",  1),
        ("oe", 1)
    ]),
    ("data", [
        ("i",  4),
        ("o",  4),
        ("oe", 1)
    ]),
    ("data_i_ce", 1),
]

_io = [
    # Clk / Rst.
    ("clk", 0, Pins(1)),
    ("rst", 1, Pins(1)),

    # Interrupt
    ("irq", 0, Pins(1)),

    # SDCard Pads.
    ("sdcard", 0,
        # Use tristate/inout-style IO

        # Subsignal("data",   Pins(4)), # Note: Requires Pullup (internal or external).
        # Subsignal("cmd",    Pins(1)), # Note: Requires Pullup (internal or external).
        # Subsignal("clk",    Pins(1)),
        # Subsignal("cd",     Pins(1)),

        # Use i/o/t-style IO (emulator's perspective)

        # Subsignal("cmd_i",  Pins(1)),
        # Subsignal("cmd_o",  Pins(1)),
        # Subsignal("cmd_t",  Pins(1)),
        # Subsignal("dat_i",  Pins(4)),
        # Subsignal("dat_o",  Pins(4)),
        # Subsignal("dat_t",  Pins(4)),
        # Subsignal("clk",    Pins(1)),
        # Subsignal("cd",     Pins(1)),

        # Use i/o/oe-style IO

        Subsignal("cmd_i",  Pins(1)),
        Subsignal("cmd_o",  Pins(1)),
        Subsignal("cmd_oe", Pins(1)),
        Subsignal("dat_i",  Pins(4)),
        Subsignal("dat_o",  Pins(4)),
        Subsignal("dat_oe", Pins(4)),
        Subsignal("clk",    Pins(1)),
        Subsignal("cd",     Pins(1)),
    ),
]


class SDPHYIOPassthrough(SDPHYIO):
    def __init__(self, clocker, sdpads, pads):
        SDPHYIO.__init__(self, clocker, sdpads, round_trip_latency=2) # FIXME: check round_trip_latency.
        # Clk
        self.comb += pads.clk.eq(clocker.clk)

        # Cmd
        self.comb += [
            sdpads.cmd.i    .eq(pads.cmd_i),
            pads.cmd_o      .eq(sdpads.cmd.o),
            pads.cmd_oe     .eq(sdpads.cmd.oe),
        ]

        # Data
        self.comb += [
            sdpads.data.i   .eq(pads.dat_i),
            pads.dat_o      .eq(sdpads.data.o),
            pads.dat_oe     .eq(sdpads.data.oe),
        ]


class SDPHY(Module, AutoCSR):
    def __init__(self, pads, device, sys_clk_freq, cmd_timeout=10e-3, data_timeout=10e-3):
        use_emulator = hasattr(pads, "cmd_t") and hasattr(pads, "dat_t")
        self.card_detect = CSRStatus() # Assume SDCard is present if no cd pin.
        self.comb += self.card_detect.status.eq(getattr(pads, "cd", 0))

        self.submodules.clocker = clocker = SDPHYClocker()
        self.submodules.init    = init    = SDPHYInit()
        self.submodules.cmdw    = cmdw    = SDPHYCMDW()
        self.submodules.cmdr    = cmdr    = SDPHYCMDR(sys_clk_freq, cmd_timeout, cmdw)
        self.submodules.dataw   = dataw   = SDPHYDATAW()
        self.submodules.datar   = datar   = SDPHYDATAR(sys_clk_freq, data_timeout)

        # # #

        self.sdpads = sdpads = Record(_sdpads_layout)

        # IOs
        # sdphy_cls = SDPHYIOEmulator if use_emulator else SDPHYIOGen
        sdphy_cls = SDPHYIOPassthrough
        self.submodules.io = sdphy_cls(clocker, sdpads, pads)

        # Connect pads_out of submodules to physical pads ----------------------------------------
        self.comb += [
            sdpads.clk.eq(    reduce(or_, [m.pads_out.clk     for m in [init, cmdw, cmdr, dataw, datar]])),
            sdpads.cmd.oe.eq( reduce(or_, [m.pads_out.cmd.oe  for m in [init, cmdw, cmdr, dataw, datar]])),
            sdpads.cmd.o.eq(  reduce(or_, [m.pads_out.cmd.o   for m in [init, cmdw, cmdr, dataw, datar]])),
            sdpads.data.oe.eq(reduce(or_, [m.pads_out.data.oe for m in [init, cmdw, cmdr, dataw, datar]])),
            sdpads.data.o.eq( reduce(or_, [m.pads_out.data.o  for m in [init, cmdw, cmdr, dataw, datar]])),
        ]
        for m in [init, cmdw, cmdr, dataw, datar]:
            self.comb += m.pads_out.ready.eq(self.clocker.ce)
        self.comb += self.clocker.clk_en.eq(sdpads.clk)

        # Connect physical pads to pads_in of submodules -------------------------------------------
        for m in [init, cmdw, cmdr, dataw, datar]:
            self.comb += m.pads_in.valid.eq(sdpads.data_i_ce)
            self.comb += m.pads_in.cmd.i.eq(sdpads.cmd.i)
            self.comb += m.pads_in.data.i.eq(sdpads.data.i)


        # Speed Throttling -------------------------------------------------------------------------
        self.comb += clocker.stop.eq(dataw.stop | datar.stop)

        # IRQs -------------------------------------------------------------------------------------
        self.card_detect_irq = Signal() # Generate Card Detect IRQ on level change.
        card_detect_d = Signal()
        self.sync += card_detect_d.eq(self.card_detect.status)
        self.sync += self.card_detect_irq.eq(self.card_detect.status ^ card_detect_d)


class LiteSDCardCore(SoCMini):
    def __init__(self, platform, clk_freq=int(100e6)):
        # CRG --------------------------------------------------------------------------------------
        self.submodules.crg = CRG(platform.request("clk"), platform.request("rst"))

        # SoCMini ----------------------------------------------------------------------------------
        SoCMini.__init__(self, platform, clk_freq=clk_freq)

        # Wishbone Control -------------------------------------------------------------------------
        # Create Wishbone Control Slave interface, expose it and connect it to the SoC.
        wb_ctrl = wishbone.Interface()
        self.add_wb_master(wb_ctrl)
        platform.add_extension(wb_ctrl.get_ios("wb_ctrl"))
        self.comb += wb_ctrl.connect_to_pads(self.platform.request("wb_ctrl"), mode="slave")

        # Wishbone DMA -----------------------------------------------------------------------------
        # Create Wishbone DMA Master interface and expose it.
        wb_dma = wishbone.Interface(data_width=32)
        platform.add_extension(wb_ctrl.get_ios("wb_dma"))
        self.comb += wb_dma.connect_to_pads(self.platform.request("wb_dma"), mode="master")

        # Create DMA Bus Handler (DMAs will be added by add_sdcard to it) and connect it to Wishbone DMA.
        self.submodules.dma_bus = SoCBusHandler(
            name             = "SoCDMABusHandler",
            standard         = "wishbone",
            data_width       = 32,
            address_width    = 32,
        )
        self.dma_bus.add_slave("dma", slave=wb_dma, region=SoCRegion(origin=0x00000000, size=0x100000000))

        # SDCard -----------------------------------------------------------------------------------
        # Simply integrate SDCard through LiteX's add_sdcard method.
        self.add_sdcard(name="sdcard")

        # IRQ
        irq_pad = platform.request("irq")
        self.comb += irq_pad.eq(self.sdirq.irq)

    def add_sdcard(self, name="sdcard", mode="read+write", use_emulator=False, software_debug=False):
        # Checks.
        assert mode in ["read", "write", "read+write"]

        # Emulator / Pads.
        if use_emulator:
            sdemulator = SDEmulator(self.platform)
            self.submodules += sdemulator
            sdcard_pads = sdemulator.pads
        else:
            sdcard_pads = self.platform.request(name)

        # Core.
        self.check_if_exists("sdphy")
        self.check_if_exists("sdcore")
        self.submodules.sdphy  = SDPHY(sdcard_pads, self.platform.device, self.clk_freq, cmd_timeout=10e-1, data_timeout=10e-1)
        self.submodules.sdcore = SDCore(self.sdphy)

        # Block2Mem DMA.
        if "read" in mode:
            bus = wishbone.Interface(data_width=self.bus.data_width, adr_width=self.bus.get_address_width(standard="wishbone"))
            self.submodules.sdblock2mem = SDBlock2MemDMA(bus=bus, endianness=self.cpu.endianness)
            self.comb += self.sdcore.source.connect(self.sdblock2mem.sink)
            dma_bus = self.bus if not hasattr(self, "dma_bus") else self.dma_bus
            dma_bus.add_master("sdblock2mem", master=bus)

        # Mem2Block DMA.
        if "write" in mode:
            bus = wishbone.Interface(data_width=self.bus.data_width, adr_width=self.bus.get_address_width(standard="wishbone"))
            self.submodules.sdmem2block = SDMem2BlockDMA(bus=bus, endianness=self.cpu.endianness)
            self.comb += self.sdmem2block.source.connect(self.sdcore.sink)
            dma_bus = self.bus if not hasattr(self, "dma_bus") else self.dma_bus
            dma_bus.add_master("sdmem2block", master=bus)

        # Interrupts.
        self.submodules.sdirq  = EventManager()
        self.sdirq.card_detect = EventSourcePulse(description="SDCard has been ejected/inserted.")
        if "read" in mode:
            self.sdirq.block2mem_dma = EventSourcePulse(description="Block2Mem DMA terminated.")
        if "write" in mode:
            self.sdirq.mem2block_dma = EventSourcePulse(description="Mem2Block DMA terminated.")
        self.sdirq.cmd_done  = EventSourceLevel(description="Command completed.")
        self.sdirq.finalize()
        if "read" in mode:
            self.comb += self.sdirq.block2mem_dma.trigger.eq(self.sdblock2mem.irq)
        if "write" in mode:
            self.comb += self.sdirq.mem2block_dma.trigger.eq(self.sdmem2block.irq)
        self.comb += [
            self.sdirq.card_detect.trigger.eq(self.sdphy.card_detect_irq),
            self.sdirq.cmd_done.trigger.eq(self.sdcore.cmd_event.fields.done)
        ]
        if self.irq.enabled:
            self.irq.add("sdirq", use_loc_if_exists=True)

        # Debug.
        if software_debug:
            self.add_constant("SDCARD_DEBUG")


def main():
    parser = argparse.ArgumentParser(description="LiteSDCard standalone core generator.")
    parser.add_argument("--clk-freq", default="100e6",  help="Input Clk Frequency.")
    parser.add_argument("--vendor",   default="xilinx", help="FPGA Vendor.")
    args = parser.parse_args()

    # Convert/Check Arguments ----------------------------------------------------------------------------
    clk_freq     = int(float(args.clk_freq))
    platform_cls = {
        "xilinx"  : XilinxPlatform,
        "altera"  : AlteraPlatform,
        "intel"   : AlteraPlatform,
        "lattice" : LatticePlatform
    }[args.vendor]

    # Generate core --------------------------------------------------------------------------------
    platform = platform_cls(device="", io=_io)
    core     = LiteSDCardCore(platform, clk_freq=clk_freq)
    builder  = Builder(core, output_dir="build/sdcard", csr_json="build/sdcard/csr.json")
    builder.build(build_name="litesdcard_core", run=False)


if __name__ == "__main__":
    main()
