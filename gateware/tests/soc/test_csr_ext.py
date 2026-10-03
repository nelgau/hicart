from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth.sim import *
from amaranth_soc import csr
from amaranth_soc.memory import MemoryMap

from hicart.soc import csr_ext
from hicart.utils.sim import MultiProcessTestCase


class _NoStorageMockRegister(wiring.Component):
    def __init__(self, width, access):
        super().__init__({"element": In(csr.Element.Signature(width, access))})

    def elaborate(self, platform):
        return Module()


class _StorageMockRegister(wiring.Component):
    def __init__(self, width, name):
        super().__init__({
            "element": In(csr.Element.Signature(width, "rw")),
            "r_count": Out(unsigned(8)),
            "w_count": Out(unsigned(8)),
            "data":    Out(width)
        })
        self._name = name

    def elaborate(self, platform):
        m = Module()

        with m.If(self.element.r_stb):
            m.d.sync += self.r_count.eq(self.r_count + 1)
        m.d.comb += self.element.r_data.eq(self.data)

        with m.If(self.element.w_stb):
            m.d.sync += self.w_count.eq(self.w_count + 1)
            m.d.sync += self.data.eq(self.element.w_data)

        return m

    def __repr__(self):
        return f"_StorageMockRegister('{self._name}')"


# Original test cases from Amaranth SOC

class MultiplexerLittleEndianTestCase(MultiProcessTestCase):

    def test_sim(self):
        for shadow_overlaps in [None, 0, 1]:
            with self.subTest(shadow_overlaps=shadow_overlaps):
                reg_4_r   = _NoStorageMockRegister( 4, "r")
                reg_8_w   = _NoStorageMockRegister( 8, "w")
                reg_16_rw = _NoStorageMockRegister(16, "rw")

                memory_map = MemoryMap(addr_width=16, data_width=8)
                memory_map.add_resource(reg_4_r,   name=("reg_4_r",),   size=1)
                memory_map.add_resource(reg_8_w,   name=("reg_8_w",),   size=1)
                memory_map.add_resource(reg_16_rw, name=("reg_16_rw",), size=2)

                dut = csr_ext.Multiplexer(memory_map, shadow_overlaps=shadow_overlaps,
                                          byteorder="little")

                async def testbench(ctx):
                    ctx.set(reg_4_r.element.r_data, 0xa)
                    ctx.set(reg_16_rw.element.r_data, 0x5aa5)

                    ctx.set(dut.bus.addr, 0)
                    ctx.set(dut.bus.r_stb, 1)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_4_r.element.r_stb), 1)
                    self.assertEqual(ctx.get(reg_16_rw.element.r_stb), 0)
                    self.assertEqual(ctx.get(dut.bus.r_data), 0xa)

                    ctx.set(dut.bus.addr, 2)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_4_r.element.r_stb), 0)
                    self.assertEqual(ctx.get(reg_16_rw.element.r_stb), 1)
                    self.assertEqual(ctx.get(dut.bus.r_data), 0xa5)

                    ctx.set(dut.bus.addr, 3) # pipeline a read
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_4_r.element.r_stb), 0)
                    self.assertEqual(ctx.get(reg_16_rw.element.r_stb), 0)
                    self.assertEqual(ctx.get(dut.bus.r_data), 0x5a)
                    ctx.set(dut.bus.r_stb, 0)

                    ctx.set(dut.bus.addr, 1)
                    ctx.set(dut.bus.w_data, 0x3d)
                    ctx.set(dut.bus.w_stb, 1)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_8_w.element.w_stb), 1)
                    self.assertEqual(ctx.get(reg_8_w.element.w_data), 0x3d)
                    self.assertEqual(ctx.get(reg_16_rw.element.w_stb), 0)

                    ctx.set(dut.bus.w_stb, 0)
                    ctx.set(dut.bus.addr, 2) # change address
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_8_w.element.w_stb), 0)

                    ctx.set(dut.bus.addr, 2)
                    ctx.set(dut.bus.w_data, 0x55)
                    ctx.set(dut.bus.w_stb, 1)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_8_w.element.w_stb), 0)
                    self.assertEqual(ctx.get(reg_16_rw.element.w_stb), 0)
                    ctx.set(dut.bus.addr, 3) # pipeline a write
                    ctx.set(dut.bus.w_data, 0xaa)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_8_w.element.w_stb), 0)
                    self.assertEqual(ctx.get(reg_16_rw.element.w_stb), 1)
                    self.assertEqual(ctx.get(reg_16_rw.element.w_data), 0xaa55)

                    ctx.set(dut.bus.addr, 2)
                    ctx.set(dut.bus.r_stb, 1)
                    ctx.set(dut.bus.w_data, 0x66)
                    ctx.set(dut.bus.w_stb, 1)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_16_rw.element.r_stb), 1)
                    self.assertEqual(ctx.get(reg_16_rw.element.w_stb), 0)
                    self.assertEqual(ctx.get(dut.bus.r_data), 0xa5)
                    ctx.set(dut.bus.addr, 3) # pipeline a read and a write
                    ctx.set(dut.bus.w_data, 0xbb)
                    await ctx.tick()
                    self.assertEqual(ctx.get(dut.bus.r_data), 0x5a)
                    self.assertEqual(ctx.get(reg_16_rw.element.r_stb), 0)
                    self.assertEqual(ctx.get(reg_16_rw.element.w_stb), 1)
                    self.assertEqual(ctx.get(reg_16_rw.element.w_data), 0xbb66)

                m = Module()
                m.submodules.reg_4_r = reg_4_r
                m.submodules.reg_8_w = reg_8_w
                m.submodules.reg_16_rw = reg_16_rw
                m.submodules.dut = dut

                with self.simulate(m) as sim:
                    sim.add_clock(1e-6)
                    sim.add_testbench(testbench)


class MultiplexerLittleEndianAlignedTestCase(MultiProcessTestCase):

    def test_sim(self):
        for shadow_overlaps in [None, 0, 1]:
            with self.subTest(shadow_overlaps=shadow_overlaps):
                reg_20_rw = _NoStorageMockRegister(20, "rw")
                memory_map = MemoryMap(addr_width=16, data_width=8, alignment=2)
                memory_map.add_resource(reg_20_rw, name=("reg_20_rw",), size=3)

                dut = csr_ext.Multiplexer(memory_map, shadow_overlaps=shadow_overlaps,
                                          byteorder="little")

                async def testbench(ctx):
                    ctx.set(dut.bus.w_stb, 1)
                    ctx.set(dut.bus.addr, 0)
                    ctx.set(dut.bus.w_data, 0x55)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_20_rw.element.w_stb), 0)
                    ctx.set(dut.bus.addr, 1)
                    ctx.set(dut.bus.w_data, 0xaa)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_20_rw.element.w_stb), 0)
                    ctx.set(dut.bus.addr, 2)
                    ctx.set(dut.bus.w_data, 0x33)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_20_rw.element.w_stb), 0)
                    ctx.set(dut.bus.addr, 3)
                    ctx.set(dut.bus.w_data, 0xdd)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_20_rw.element.w_stb), 1)
                    self.assertEqual(ctx.get(reg_20_rw.element.w_data), 0x3aa55)

                m = Module()
                m.submodules.reg_20_rw = reg_20_rw
                m.submodules.dut = dut

                with self.simulate(m) as sim:
                    sim.add_clock(1e-6)
                    sim.add_testbench(testbench)


class WishboneCSRBridgeLittleEndianTestCase(MultiProcessTestCase):

    def test_narrow(self):
        reg_1 = _StorageMockRegister( 8, name="reg_1")
        reg_2 = _StorageMockRegister(16, name="reg_2")

        memory_map = MemoryMap(addr_width=10, data_width=8)
        memory_map.add_resource(reg_1, name=("reg_1",), size=1)
        memory_map.add_resource(reg_2, name=("reg_2",), size=2)

        mux = csr_ext.Multiplexer(memory_map, byteorder="little")
        dut = csr_ext.WishboneCSRBridge(mux.bus, byteorder="little")

        async def testbench(ctx):
            ctx.set(dut.wb_bus.cyc, 1)
            ctx.set(dut.wb_bus.sel, 0b1)
            ctx.set(dut.wb_bus.we, 1)

            ctx.set(dut.wb_bus.adr, 0)
            ctx.set(dut.wb_bus.stb, 1)
            ctx.set(dut.wb_bus.dat_w, 0x55)
            await ctx.tick().repeat(2)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg_1.r_count), 0)
            self.assertEqual(ctx.get(reg_1.w_count), 1)
            self.assertEqual(ctx.get(reg_1.data), 0x55)

            ctx.set(dut.wb_bus.adr, 1)
            ctx.set(dut.wb_bus.stb, 1)
            ctx.set(dut.wb_bus.dat_w, 0xaa)
            await ctx.tick().repeat(2)
            ctx.set(dut.wb_bus.stb, 0)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg_2.r_count), 0)
            self.assertEqual(ctx.get(reg_2.w_count), 0)
            self.assertEqual(ctx.get(reg_2.data), 0)

            ctx.set(dut.wb_bus.adr, 2)
            ctx.set(dut.wb_bus.stb, 1)
            ctx.set(dut.wb_bus.dat_w, 0xbb)
            await ctx.tick().repeat(2)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg_2.r_count), 0)
            self.assertEqual(ctx.get(reg_2.w_count), 1)
            self.assertEqual(ctx.get(reg_2.data), 0xbbaa)

            ctx.set(dut.wb_bus.we, 0)

            ctx.set(dut.wb_bus.adr, 0)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(2)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            self.assertEqual(ctx.get(dut.wb_bus.dat_r), 0x55)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg_1.r_count), 1)
            self.assertEqual(ctx.get(reg_1.w_count), 1)

            ctx.set(dut.wb_bus.adr, 1)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(2)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            self.assertEqual(ctx.get(dut.wb_bus.dat_r), 0xaa)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg_2.r_count), 1)
            self.assertEqual(ctx.get(reg_2.w_count), 1)

            ctx.set(reg_2.data, 0x33333)

            ctx.set(dut.wb_bus.adr, 2)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(2)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            self.assertEqual(ctx.get(dut.wb_bus.dat_r), 0xbb)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg_2.r_count), 1)
            self.assertEqual(ctx.get(reg_2.w_count), 1)

        m = Module()
        m.submodules.reg_1 = reg_1
        m.submodules.reg_2 = reg_2
        m.submodules.mux = mux
        m.submodules.dut = dut

        with self.simulate(m) as sim:
            sim.add_clock(1e-6)
            sim.add_testbench(testbench)

    def test_wide(self):
        reg = _StorageMockRegister(32, name="reg")

        memory_map = MemoryMap(addr_width=10, data_width=8)
        memory_map.add_resource(reg, name=("reg",), size=4)

        mux = csr_ext.Multiplexer(memory_map, byteorder="little")
        dut = csr_ext.WishboneCSRBridge(mux.bus, data_width=32, byteorder="little")

        async def testbench(ctx):
            ctx.set(dut.wb_bus.cyc, 1)
            ctx.set(dut.wb_bus.adr, 0)
            ctx.set(dut.wb_bus.we, 1)

            ctx.set(dut.wb_bus.dat_w, 0x44332211)
            ctx.set(dut.wb_bus.sel, 0b1111)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(5)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg.r_count), 0)
            self.assertEqual(ctx.get(reg.w_count), 1)
            self.assertEqual(ctx.get(reg.data), 0x44332211)

            # partial write
            ctx.set(dut.wb_bus.dat_w, 0xaabbccdd)
            ctx.set(dut.wb_bus.sel, 0b0110)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(5)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg.r_count), 0)
            self.assertEqual(ctx.get(reg.w_count), 1)
            self.assertEqual(ctx.get(reg.data), 0x44332211)

            ctx.set(dut.wb_bus.we, 0)

            ctx.set(dut.wb_bus.sel, 0b1111)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(5)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            self.assertEqual(ctx.get(dut.wb_bus.dat_r), 0x44332211)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg.r_count), 1)
            self.assertEqual(ctx.get(reg.w_count), 1)

            ctx.set(reg.data, 0xaaaaaaaa)

            # partial read
            ctx.set(dut.wb_bus.sel, 0b0110)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(5)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            self.assertEqual(ctx.get(dut.wb_bus.dat_r), 0x00332200)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg.r_count), 1)
            self.assertEqual(ctx.get(reg.w_count), 1)

        m = Module()
        m.submodules.reg = reg
        m.submodules.mux = mux
        m.submodules.dut = dut

        with self.simulate(m) as sim:
            sim.add_clock(1e-6)
            sim.add_testbench(testbench)


# Added test cases specifically targetting big endian operation

class MultiplexerBigEndianTestCase(MultiProcessTestCase):

    def test_sim(self):
        for shadow_overlaps in [None, 0, 1]:
            with self.subTest(shadow_overlaps=shadow_overlaps):
                reg_4_r   = _NoStorageMockRegister( 4, "r")
                reg_8_w   = _NoStorageMockRegister( 8, "w")
                reg_16_rw = _NoStorageMockRegister(16, "rw")

                memory_map = MemoryMap(addr_width=16, data_width=8)
                memory_map.add_resource(reg_4_r,   name=("reg_4_r",),   size=1)
                memory_map.add_resource(reg_8_w,   name=("reg_8_w",),   size=1)
                memory_map.add_resource(reg_16_rw, name=("reg_16_rw",), size=2)

                dut = csr_ext.Multiplexer(memory_map, shadow_overlaps=shadow_overlaps,
                                          byteorder="big")

                async def testbench(ctx):
                    ctx.set(reg_4_r.element.r_data, 0xa)
                    ctx.set(reg_16_rw.element.r_data, 0x5aa5)

                    ctx.set(dut.bus.addr, 0)
                    ctx.set(dut.bus.r_stb, 1)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_4_r.element.r_stb), 1)
                    self.assertEqual(ctx.get(reg_16_rw.element.r_stb), 0)
                    self.assertEqual(ctx.get(dut.bus.r_data), 0xa)

                    ctx.set(dut.bus.addr, 2)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_4_r.element.r_stb), 0)
                    self.assertEqual(ctx.get(reg_16_rw.element.r_stb), 1)
                    self.assertEqual(ctx.get(dut.bus.r_data), 0x5a)

                    ctx.set(dut.bus.addr, 3) # pipeline a read
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_4_r.element.r_stb), 0)
                    self.assertEqual(ctx.get(reg_16_rw.element.r_stb), 0)
                    self.assertEqual(ctx.get(dut.bus.r_data), 0xa5)
                    ctx.set(dut.bus.r_stb, 0)

                    ctx.set(dut.bus.addr, 1)
                    ctx.set(dut.bus.w_data, 0x3d)
                    ctx.set(dut.bus.w_stb, 1)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_8_w.element.w_stb), 1)
                    self.assertEqual(ctx.get(reg_8_w.element.w_data), 0x3d)
                    self.assertEqual(ctx.get(reg_16_rw.element.w_stb), 0)

                    ctx.set(dut.bus.w_stb, 0)
                    ctx.set(dut.bus.addr, 2) # change address
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_8_w.element.w_stb), 0)

                    ctx.set(dut.bus.addr, 2)
                    ctx.set(dut.bus.w_data, 0x55)
                    ctx.set(dut.bus.w_stb, 1)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_8_w.element.w_stb), 0)
                    self.assertEqual(ctx.get(reg_16_rw.element.w_stb), 0)
                    ctx.set(dut.bus.addr, 3) # pipeline a write
                    ctx.set(dut.bus.w_data, 0xaa)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_8_w.element.w_stb), 0)
                    self.assertEqual(ctx.get(reg_16_rw.element.w_stb), 1)
                    self.assertEqual(ctx.get(reg_16_rw.element.w_data), 0x55aa)

                    ctx.set(dut.bus.addr, 2)
                    ctx.set(dut.bus.r_stb, 1)
                    ctx.set(dut.bus.w_data, 0x66)
                    ctx.set(dut.bus.w_stb, 1)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_16_rw.element.r_stb), 1)
                    self.assertEqual(ctx.get(reg_16_rw.element.w_stb), 0)
                    self.assertEqual(ctx.get(dut.bus.r_data), 0x5a)
                    ctx.set(dut.bus.addr, 3) # pipeline a read and a write
                    ctx.set(dut.bus.w_data, 0xbb)
                    await ctx.tick()
                    self.assertEqual(ctx.get(dut.bus.r_data), 0xa5)
                    self.assertEqual(ctx.get(reg_16_rw.element.r_stb), 0)
                    self.assertEqual(ctx.get(reg_16_rw.element.w_stb), 1)
                    self.assertEqual(ctx.get(reg_16_rw.element.w_data), 0x66bb)

                m = Module()
                m.submodules.reg_4_r = reg_4_r
                m.submodules.reg_8_w = reg_8_w
                m.submodules.reg_16_rw = reg_16_rw
                m.submodules.dut = dut

                with self.simulate(m) as sim:
                    sim.add_clock(1e-6)
                    sim.add_testbench(testbench)


class MultiplexerBigEndianAlignedTestCase(MultiProcessTestCase):

    def test_sim(self):
        for shadow_overlaps in [None, 0, 1]:
            with self.subTest(shadow_overlaps=shadow_overlaps):
                reg_20_rw = _NoStorageMockRegister(20, "rw")
                memory_map = MemoryMap(addr_width=16, data_width=8, alignment=2)
                memory_map.add_resource(reg_20_rw, name=("reg_20_rw",), size=3)

                dut = csr_ext.Multiplexer(memory_map, shadow_overlaps=shadow_overlaps,
                                          byteorder="big")

                async def testbench(ctx):
                    ctx.set(dut.bus.w_stb, 1)
                    ctx.set(dut.bus.addr, 0)
                    ctx.set(dut.bus.w_data, 0x55)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_20_rw.element.w_stb), 0)
                    ctx.set(dut.bus.addr, 1)
                    ctx.set(dut.bus.w_data, 0xaa)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_20_rw.element.w_stb), 0)
                    ctx.set(dut.bus.addr, 2)
                    ctx.set(dut.bus.w_data, 0x33)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_20_rw.element.w_stb), 0)
                    ctx.set(dut.bus.addr, 3)
                    ctx.set(dut.bus.w_data, 0xdd)
                    await ctx.tick()
                    self.assertEqual(ctx.get(reg_20_rw.element.w_stb), 1)
                    self.assertEqual(ctx.get(reg_20_rw.element.w_data), 0xa33dd)

                m = Module()
                m.submodules.reg_20_rw = reg_20_rw
                m.submodules.dut = dut

                with self.simulate(m) as sim:
                    sim.add_clock(1e-6)
                    sim.add_testbench(testbench)


class WishboneCSRBridgeBigEndianTestCase(MultiProcessTestCase):

    def test_narrow(self):
        reg_1 = _StorageMockRegister( 8, name="reg_1")
        reg_2 = _StorageMockRegister(16, name="reg_2")

        memory_map = MemoryMap(addr_width=10, data_width=8)
        memory_map.add_resource(reg_1, name=("reg_1",), size=1)
        memory_map.add_resource(reg_2, name=("reg_2",), size=2)

        mux = csr_ext.Multiplexer(memory_map, byteorder="big")
        dut = csr_ext.WishboneCSRBridge(mux.bus, byteorder="big")

        async def testbench(ctx):
            ctx.set(dut.wb_bus.cyc, 1)
            ctx.set(dut.wb_bus.sel, 0b1)
            ctx.set(dut.wb_bus.we, 1)

            ctx.set(dut.wb_bus.adr, 0)
            ctx.set(dut.wb_bus.stb, 1)
            ctx.set(dut.wb_bus.dat_w, 0x55)
            await ctx.tick().repeat(2)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg_1.r_count), 0)
            self.assertEqual(ctx.get(reg_1.w_count), 1)
            self.assertEqual(ctx.get(reg_1.data), 0x55)

            ctx.set(dut.wb_bus.adr, 1)
            ctx.set(dut.wb_bus.stb, 1)
            ctx.set(dut.wb_bus.dat_w, 0xaa)
            await ctx.tick().repeat(2)
            ctx.set(dut.wb_bus.stb, 0)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg_2.r_count), 0)
            self.assertEqual(ctx.get(reg_2.w_count), 0)
            self.assertEqual(ctx.get(reg_2.data), 0)

            ctx.set(dut.wb_bus.adr, 2)
            ctx.set(dut.wb_bus.stb, 1)
            ctx.set(dut.wb_bus.dat_w, 0xbb)
            await ctx.tick().repeat(2)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg_2.r_count), 0)
            self.assertEqual(ctx.get(reg_2.w_count), 1)
            self.assertEqual(ctx.get(reg_2.data), 0xaabb)

            ctx.set(dut.wb_bus.we, 0)

            ctx.set(dut.wb_bus.adr, 0)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(2)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            self.assertEqual(ctx.get(dut.wb_bus.dat_r), 0x55)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg_1.r_count), 1)
            self.assertEqual(ctx.get(reg_1.w_count), 1)

            ctx.set(dut.wb_bus.adr, 1)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(2)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            self.assertEqual(ctx.get(dut.wb_bus.dat_r), 0xaa)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg_2.r_count), 1)
            self.assertEqual(ctx.get(reg_2.w_count), 1)

            ctx.set(reg_2.data, 0x33333)

            ctx.set(dut.wb_bus.adr, 2)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(2)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            self.assertEqual(ctx.get(dut.wb_bus.dat_r), 0xbb)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg_2.r_count), 1)
            self.assertEqual(ctx.get(reg_2.w_count), 1)

        m = Module()
        m.submodules.reg_1 = reg_1
        m.submodules.reg_2 = reg_2
        m.submodules.mux = mux
        m.submodules.dut = dut

        with self.simulate(m) as sim:
            sim.add_clock(1e-6)
            sim.add_testbench(testbench)

    def test_wide(self):
        reg = _StorageMockRegister(32, name="reg")

        memory_map = MemoryMap(addr_width=10, data_width=8)
        memory_map.add_resource(reg, name=("reg",), size=4)

        mux = csr_ext.Multiplexer(memory_map, byteorder="big")
        dut = csr_ext.WishboneCSRBridge(mux.bus, data_width=32, byteorder="big")

        async def testbench(ctx):
            ctx.set(dut.wb_bus.cyc, 1)
            ctx.set(dut.wb_bus.adr, 0)
            ctx.set(dut.wb_bus.we, 1)

            ctx.set(dut.wb_bus.dat_w, 0x44332211)
            ctx.set(dut.wb_bus.sel, 0b1111)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(5)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg.r_count), 0)
            self.assertEqual(ctx.get(reg.w_count), 1)
            self.assertEqual(ctx.get(reg.data), 0x44332211)

            # partial write
            ctx.set(dut.wb_bus.dat_w, 0xaabbccdd)
            ctx.set(dut.wb_bus.sel, 0b0110)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(5)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg.r_count), 0)
            self.assertEqual(ctx.get(reg.w_count), 1)
            self.assertEqual(ctx.get(reg.data), 0x44332211)

            ctx.set(dut.wb_bus.we, 0)

            ctx.set(dut.wb_bus.sel, 0b1111)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(5)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            self.assertEqual(ctx.get(dut.wb_bus.dat_r), 0x44332211)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg.r_count), 1)
            self.assertEqual(ctx.get(reg.w_count), 1)

            ctx.set(reg.data, 0xaaaaaaaa)

            # partial read
            ctx.set(dut.wb_bus.sel, 0b0110)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(5)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            self.assertEqual(ctx.get(dut.wb_bus.dat_r), 0x00332200)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg.r_count), 1)
            self.assertEqual(ctx.get(reg.w_count), 1)

        m = Module()
        m.submodules.reg = reg
        m.submodules.mux = mux
        m.submodules.dut = dut

        with self.simulate(m) as sim:
            sim.add_clock(1e-6)
            sim.add_testbench(testbench)


class SpecificCSRTestCase(MultiProcessTestCase):

    def test_read_order(self):
        reg = _NoStorageMockRegister(32, "r")

        memory_map = MemoryMap(addr_width=32, data_width=8)
        memory_map.add_resource(reg, name="reg", size=4)

        mux = csr_ext.Multiplexer(memory_map, byteorder="big")
        dut = csr_ext.WishboneCSRBridge(mux.bus, data_width=16, byteorder="big")

        async def testbench(ctx):
            ctx.set(reg.element.r_data, 0x12345678)

            ctx.set(dut.wb_bus.cyc, 1)
            ctx.set(dut.wb_bus.we, 0)
            ctx.set(dut.wb_bus.sel, 0b1111)

            ctx.set(dut.wb_bus.adr, 0)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(3)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            self.assertEqual(ctx.get(dut.wb_bus.dat_r), 0x1234)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)

            ctx.set(dut.wb_bus.adr, 1)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(3)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            self.assertEqual(ctx.get(dut.wb_bus.dat_r), 0x5678)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)

        m = Module()
        m.submodules.reg = reg
        m.submodules.mux = mux
        m.submodules.dut = dut

        with self.simulate(m) as sim:
            sim.add_clock(1e-6)
            sim.add_testbench(testbench)

    def test_read_atomicity(self):
        reg = _NoStorageMockRegister(32, "r")

        memory_map = MemoryMap(addr_width=32, data_width=8)
        memory_map.add_resource(reg, name="reg", size=4)

        mux = csr_ext.Multiplexer(memory_map, byteorder="big")
        dut = csr_ext.WishboneCSRBridge(mux.bus, data_width=16, byteorder="big")

        async def testbench(ctx):
            ctx.set(reg.element.r_data, 0x12345678)

            ctx.set(dut.wb_bus.cyc, 1)
            ctx.set(dut.wb_bus.we, 0)
            ctx.set(dut.wb_bus.sel, 0b1111)

            ctx.set(dut.wb_bus.adr, 0)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(3)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            self.assertEqual(ctx.get(dut.wb_bus.dat_r), 0x1234)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)

            ctx.set(reg.element.r_data, 0xAAAABBBB)

            ctx.set(dut.wb_bus.adr, 1)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(3)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            self.assertEqual(ctx.get(dut.wb_bus.dat_r), 0x5678)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)

        m = Module()
        m.submodules.reg = reg
        m.submodules.mux = mux
        m.submodules.dut = dut

        with self.simulate(m) as sim:
            sim.add_clock(1e-6)
            sim.add_testbench(testbench)

    def test_write_commits_on_last_chunk(self):
        reg = _StorageMockRegister(32, "r")

        memory_map = MemoryMap(addr_width=32, data_width=8)
        memory_map.add_resource(reg, name="reg", size=4)

        mux = csr_ext.Multiplexer(memory_map, byteorder="big")
        dut = csr_ext.WishboneCSRBridge(mux.bus, data_width=16, byteorder="big")

        async def testbench(ctx):
            ctx.set(reg.data, 0xDEADBEEF)

            ctx.set(dut.wb_bus.cyc, 1)
            ctx.set(dut.wb_bus.we, 1)
            ctx.set(dut.wb_bus.sel, 0b1111)

            ctx.set(dut.wb_bus.adr, 0)
            ctx.set(dut.wb_bus.dat_w, 0XABCD)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(3)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg.r_count), 0)
            self.assertEqual(ctx.get(reg.w_count), 0)

            self.assertEqual(ctx.get(reg.data), 0xDEADBEEF)

            ctx.set(dut.wb_bus.adr, 1)
            ctx.set(dut.wb_bus.dat_w, 0XEF01)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(3)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg.r_count), 0)
            self.assertEqual(ctx.get(reg.w_count), 1)

            self.assertEqual(ctx.get(reg.data), 0xABCDEF01)

        m = Module()
        m.submodules.reg = reg
        m.submodules.mux = mux
        m.submodules.dut = dut

        with self.simulate(m) as sim:
            sim.add_clock(1e-6)
            sim.add_testbench(testbench)

    def test_out_of_order(self):
        reg = _StorageMockRegister(32, "r")

        memory_map = MemoryMap(addr_width=32, data_width=8)
        memory_map.add_resource(reg, name="reg", size=4)

        mux = csr_ext.Multiplexer(memory_map, byteorder="big")
        dut = csr_ext.WishboneCSRBridge(mux.bus, data_width=16, byteorder="big")

        async def testbench(ctx):
            ctx.set(dut.wb_bus.cyc, 1)
            ctx.set(dut.wb_bus.we, 0)
            ctx.set(dut.wb_bus.sel, 0b1111)

            ctx.set(dut.wb_bus.adr, 1)
            ctx.set(dut.wb_bus.stb, 1)
            await ctx.tick().repeat(3)
            self.assertEqual(ctx.get(dut.wb_bus.ack), 1)
            ctx.set(dut.wb_bus.stb, 0)
            await ctx.tick()
            self.assertEqual(ctx.get(dut.wb_bus.ack), 0)
            self.assertEqual(ctx.get(reg.r_count), 0)
            self.assertEqual(ctx.get(reg.w_count), 0)

        m = Module()
        m.submodules.reg = reg
        m.submodules.mux = mux
        m.submodules.dut = dut

        with self.simulate(m) as sim:
            sim.add_clock(1e-6)
            sim.add_testbench(testbench)
