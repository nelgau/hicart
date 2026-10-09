from amaranth import *
from amaranth.lib import stream, wiring
from amaranth.lib.memory import Memory, MemoryData
from amaranth.lib.wiring import In, Out, flipped
from amaranth.utils import exact_log2
from amaranth_soc import csr, wishbone
from amaranth_soc.memory import MemoryMap

from hicart.soc import csr_ext


class SDBuffer(wiring.Component):

    class WriterBusSignature(wiring.Signature):

        def __init__(self, *, addr_width, data_width):
            self._addr_width = addr_width
            self._data_width = data_width

            super().__init__({
                "addr": Out(addr_width),
                "w_data": Out(data_width),
                "w_stb": Out(1),
            })

        @property
        def addr_width(self):
            return self._addr_width

        @property
        def data_width(self):
            return self._data_width

    def __init__(self, *, num_sectors=8, host_domain="sync", sys_domain="sync"):
        if num_sectors & (num_sectors - 1) != 0:
            raise ValueError("Number of sectors must be a power of two")

        self._host_domain = host_domain
        self._sys_domain = sys_domain

        self._size = 512 * num_sectors
        data_width = 16
        granularity = 8

        self._mem_data = MemoryData(depth=(self._size * granularity) // data_width,
                                    shape=unsigned(data_width), init=())
        self._mem = Memory(self._mem_data)

        super().__init__({
            "wb_bus": In(wishbone.Signature(addr_width=exact_log2(self._mem.depth),
                                            data_width=data_width,
                                            granularity=granularity)),

            "writer_bus": In(self.WriterBusSignature(addr_width=exact_log2(self._size),
                                                     data_width=granularity))
        })
        self.wb_bus.memory_map = MemoryMap(addr_width=exact_log2(self._size), data_width=granularity)
        self.wb_bus.memory_map.add_resource(self._mem, name=("sectors",), size=self._size)
        self.wb_bus.memory_map.freeze()

    @property
    def size(self):
        return self._size

    def elaborate(self, platform):
        m = Module()
        m.submodules.mem = self._mem

        data_width = 16
        granularity = 8

        en_width = data_width // granularity
        granularity_bits = exact_log2(en_width)

        # Wishbone bus

        wb_read_port = self._mem.read_port(domain=self._host_domain)
        m.d.comb += wb_read_port.addr.eq(self.wb_bus.adr)

        # Swap lanes because host side is big-endian
        for i in range(en_width):
            value = wb_read_port.data.word_select(i, granularity)
            m.d.comb += self.wb_bus.dat_r.word_select(en_width - i - 1, granularity).eq(value)

        with m.If(self.wb_bus.ack):
            m.d.sync += self.wb_bus.ack.eq(0)
        with m.Elif(self.wb_bus.cyc & self.wb_bus.stb):
            m.d.sync += self.wb_bus.ack.eq(1)

        # Writer bus

        writer_write_port = self._mem.write_port(domain=self._sys_domain, granularity=granularity)

        m.d.comb += writer_write_port.addr.eq(self.writer_bus.addr[granularity_bits:])
        m.d.comb += writer_write_port.data.eq(self.writer_bus.w_data.replicate(en_width))

        en_index = self.writer_bus.addr[:granularity_bits]
        m.d.comb += writer_write_port.en.word_select(en_index, 1).eq(1)

        return m


class SDBufferWriter(wiring.Component):

    class Address(csr.Register, access="rw"):
        def __init__(self, addr_width, reg_width=32):
            super().__init__({
                "address": csr.Field(csr_ext.RWExtAction, unsigned(addr_width)),
                "_0": csr.Field(csr.action.R, unsigned(reg_width - addr_width)),
            })

    def __init__(self, *, writer_bus):
        self._writer_bus = writer_bus
        self._addr_width = writer_bus.signature.addr_width

        regs = csr.Builder(addr_width=8, data_width=8)
        self._address_reg = regs.add("Address", self.Address(self._addr_width))
        self._csr_bridge = csr_ext.Bridge(regs.as_memory_map(), byteorder="little")

        super().__init__({
            "sink": In(stream.Signature(8, always_ready=True)),
            "writer_bus": Out(SDBuffer.WriterBusSignature(addr_width=self._addr_width,
                                                          data_width=8)),
            "csr_bus": In(csr.Signature(addr_width=8, data_width=8)),
        })
        self.csr_bus.memory_map = self._csr_bridge.bus.memory_map

    def elaborate(self, platform):
        m = Module()
        m.submodules.csr_bridge = self._csr_bridge

        wiring.connect(m, self._csr_bridge.bus, flipped(self.csr_bus))

        address = Signal(self._addr_width)

        m.d.comb += self.writer_bus.addr.eq(address)
        m.d.comb += self.writer_bus.w_data.eq(self.sink.payload)
        m.d.comb += self.writer_bus.w_stb.eq(self.sink.valid)

        with m.If(self.sink.valid):
            m.d.sync += address.eq(address + 1)

        m.d.comb += self._address_reg.f.address.r_data.eq(address)

        with m.If(self._address_reg.f.address.w_stb):
            m.d.sync += address.eq(self._address_reg.f.address.w_data)

        return m
