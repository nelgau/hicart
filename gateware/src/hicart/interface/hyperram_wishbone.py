from amaranth import *
from amaranth_soc import wishbone
from amaranth_soc.memory import MemoryMap

from hicart.interface.hyperram import HyperBus, HyperRAMInterface


class HyperRAMWishboneInterface(Elaboratable):

    def __init__(self):
        self.hbus = HyperBus()

        self.wbus = wishbone.Interface(addr_width=32, data_width=16, features={"stall"})

        memory_map = MemoryMap(addr_width=32, data_width=16)
        memory_map.add_resource(self, size=2**32, name='hyperram')
        self.wbus.memory_map = memory_map

    def elaborate(self, platform):
        m = Module()

        m.submodules.iface = iface = HyperRAMInterface(self.hbus)

        m.d.comb += [
            iface.start_transfer        .eq(self.wbus.cyc & self.wbus.stb),        
            iface.address               .eq(self.wbus.adr),
            iface.perform_write         .eq(self.wbus.we),
            iface.write_data            .eq(self.wbus.dat_w),

            iface.register_space        .eq(0),
            iface.single_page           .eq(0),
            iface.final_word            .eq(1),

            self.wbus.stall             .eq(~iface.idle),
            self.wbus.dat_r             .eq(iface.read_data),
            self.wbus.ack               .eq(iface.new_data_ready),
        ]

        return m
