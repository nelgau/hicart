from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.memory import Memory, MemoryData
from amaranth.lib.wiring import In, Out
from amaranth.utils import exact_log2
from amaranth_soc import wishbone
from amaranth_soc.memory import MemoryMap


class StrobeBusSignature(wiring.Signature):

    def __init__(self, *, addr_width, data_width):
        super().__init__({
            "addr": Out(addr_width),
            "w_data": Out(data_width),
            "w_stb": Out(1),
        })


class SectorBuffer(wiring.Component):

    def __init__(self, *, num_sectors=8, host_domain="sync", sys_domain="sync"):
        if num_sectors & (num_sectors - 1) != 0:
            raise ValueError("Number of sectors must be a power of two")

        self._host_domain = host_domain
        self._sys_domain = sys_domain

        size = 512 * num_sectors
        data_width = 16
        granularity = 8

        self._mem_data = MemoryData(depth=(size * granularity) // data_width,
                                    shape=unsigned(data_width), init=())
        self._mem = Memory(self._mem_data)

        super().__init__({
            "wb_bus": In(wishbone.Signature(addr_width=exact_log2(self._mem.depth),
                                            data_width=data_width,
                                            granularity=granularity)),

            "stb_bus": In(StrobeBusSignature(addr_width=exact_log2(size),
                                             data_width=granularity))
        })
        self.wb_bus.memory_map = MemoryMap(addr_width=exact_log2(size), data_width=granularity)
        self.wb_bus.memory_map.add_resource(self._mem, name=("sectors",), size=size)
        self.wb_bus.memory_map.freeze()

    def elaborate(self, platform):
        m = Module()
        m.submodules.mem = self._mem

        data_width = 16
        granularity = 8

        # Wishbone bus

        wb_read_port = self._mem.read_port(domain=self._host_domain)
        m.d.comb += wb_read_port.addr.eq(self.wb_bus.adr)
        m.d.comb += self.wb_bus.dat_r.eq(wb_read_port.data)

        with m.If(self.wb_bus.ack):
            m.d.sync += self.wb_bus.ack.eq(0)
        with m.Elif(self.wb_bus.cyc & self.wb_bus.stb):
            m.d.sync += self.wb_bus.ack.eq(1)

        # Strobe bus

        stb_en_width = data_width // granularity
        stb_granularity_bits = exact_log2(stb_en_width)

        stb_write_port = self._mem.write_port(domain=self._sys_domain, granularity=granularity)

        m.d.comb += stb_write_port.addr.eq(self.stb_bus.addr[stb_granularity_bits:])
        m.d.comb += stb_write_port.data.eq(self.stb_bus.w_data.replicate(stb_en_width))

        stb_en_index = self.stb_bus.addr[:stb_granularity_bits]
        m.d.comb += stb_write_port.en.word_select(stb_en_index, 1).eq(1)

        return m
