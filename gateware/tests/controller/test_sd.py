from amaranth import *
from amaranth.sim import *

from hicart.controller import sd
from hicart.utils.sim import MultiProcessTestCase


class TestSDClocker(MultiProcessTestCase):

    def test_basic(self):
        dut = sd.Clocker()

        async def testbench(ctx):
            assert ctx.get(dut.sd_clk) == 0
            assert ctx.get(dut.sd_clk_rising) == 0
            assert ctx.get(dut.sd_clk_falling) == 0

            await ctx.tick()

            assert ctx.get(dut.sd_clk) == 0
            assert ctx.get(dut.sd_clk_rising) == 0
            assert ctx.get(dut.sd_clk_falling) == 0

            ctx.set(dut.enable, 1)
            ctx.set(dut.half_period, 5)

            assert ctx.get(dut.sd_clk) == 0
            assert ctx.get(dut.sd_clk_rising) == 1
            assert ctx.get(dut.sd_clk_falling) == 0

            await ctx.tick()

            assert ctx.get(dut.sd_clk) == 1
            assert ctx.get(dut.sd_clk_rising) == 0
            assert ctx.get(dut.sd_clk_falling) == 0

            await ctx.tick().repeat(4)

            assert ctx.get(dut.sd_clk) == 1
            assert ctx.get(dut.sd_clk_rising) == 0
            assert ctx.get(dut.sd_clk_falling) == 1

            await ctx.tick()

            assert ctx.get(dut.sd_clk) == 0
            assert ctx.get(dut.sd_clk_rising) == 0
            assert ctx.get(dut.sd_clk_falling) == 0

            await ctx.tick().repeat(4)

            assert ctx.get(dut.sd_clk) == 0
            assert ctx.get(dut.sd_clk_rising) == 1
            assert ctx.get(dut.sd_clk_falling) == 0

            await ctx.tick()

            assert ctx.get(dut.sd_clk) == 1
            assert ctx.get(dut.sd_clk_rising) == 0
            assert ctx.get(dut.sd_clk_falling) == 0

        with self.simulate(dut) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(testbench)


class TestCmdTx(MultiProcessTestCase):

    async def _receive_bytes(self, ctx, sd_clk, sd_cmd_o, sd_cmd_oe, num_bytes):
        bytes = []
        receiving = False
        byte_index = 0
        bit_index = 0
        byte = 0

        while True:
            await ctx.posedge(sd_clk)
            bit = ctx.get(Mux(sd_cmd_oe, sd_cmd_o, 1))

            if not receiving and not bit:
                receiving = True

            if receiving:
                byte = (byte << 1) | bit
                bit_index += 1

            if bit_index == 8:
                bytes.append(byte)
                byte_index += 1
                bit_index = 0
                byte = 0

            if byte_index == num_bytes:
                break

        return bytes

    def test_cmd8(self):
        clocker = sd.Clocker()
        dut = sd.CmdTx()

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += dut.sd_clk_rising.eq(clocker.sd_clk_rising)
        m.d.comb += dut.sd_clk_falling.eq(clocker.sd_clk_falling)

        async def control(ctx):
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.half_period, 2)

            ctx.set(dut.cmd_index, 8)
            ctx.set(dut.cmd_arg, 0x000001AA)
            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            await ctx.tick().until(dut.done)

        async def output(ctx):
            bytes = await self._receive_bytes(ctx, clocker.sd_clk, dut.sd_cmd_o, dut.sd_cmd_oe, 6)
            assert bytes == [0x48, 0x00, 0x00, 0x01, 0xaa, 0x87]

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(control)
            sim.add_testbench(output)

    def test_cmd8_min_half_period(self):
        clocker = sd.Clocker()
        dut = sd.CmdTx()

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += dut.sd_clk_rising.eq(clocker.sd_clk_rising)
        m.d.comb += dut.sd_clk_falling.eq(clocker.sd_clk_falling)

        async def control(ctx):
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.half_period, 1)

            ctx.set(dut.cmd_index, 8)
            ctx.set(dut.cmd_arg, 0x000001AA)
            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            await ctx.tick().until(dut.done)

        async def output(ctx):
            bytes = await self._receive_bytes(ctx, clocker.sd_clk, dut.sd_cmd_o, dut.sd_cmd_oe, 6)
            assert bytes == [0x48, 0x00, 0x00, 0x01, 0xaa, 0x87]

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(control)
            sim.add_testbench(output)


class TestCmdRx(MultiProcessTestCase):

    async def _send_frame(self, ctx, sd_clk, sd_cmd_i, frame):
        for byte in frame:
            for i in reversed(range(8)):
                bit = (byte >> i) & 0x1
                await ctx.negedge(sd_clk)
                ctx.set(sd_cmd_i, bit)

        await ctx.negedge(sd_clk)
        ctx.set(sd_cmd_i, 1)

    def test_timeout(self):
        clocker = sd.Clocker()
        dut = sd.CmdRx(timeout=64)

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += dut.sd_clk_rising.eq(clocker.sd_clk_rising)
        m.d.comb += dut.sd_clk_falling.eq(clocker.sd_clk_falling)

        async def testbench(ctx):
            ctx.set(dut.sd_cmd_i, 1)
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.half_period, 2)

            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            await ctx.tick().until(dut.done)
            assert ctx.get(dut.err_timeout) == 1

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(testbench)

    def test_short(self):
        clocker = sd.Clocker()
        dut = sd.CmdRx(timeout=64)

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += dut.sd_clk_rising.eq(clocker.sd_clk_rising)
        m.d.comb += dut.sd_clk_falling.eq(clocker.sd_clk_falling)

        frame = [0x08, 0x00, 0x00, 0x01, 0xaa, 0x13]

        async def card(ctx):
            ctx.set(dut.sd_cmd_i, 1)

            for _ in range(10):
                await ctx.posedge(clocker.sd_clk)

            await self._send_frame(ctx, clocker.sd_clk, dut.sd_cmd_i, frame)

        async def control(ctx):
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.half_period, 2)

            ctx.set(dut.long_response, 0)
            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            await ctx.tick().until(dut.done)

            assert ctx.get(dut.cmd_index) == 8
            assert ctx.get(dut.cmd_resp) == 0x000001aa

            assert ctx.get(dut.err_timeout) == 0
            assert ctx.get(dut.err_dir) == 0
            assert ctx.get(dut.err_crc) == 0
            assert ctx.get(dut.err_end) == 0

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(card)
            sim.add_testbench(control)

    def test_short_min_half_period(self):
        clocker = sd.Clocker()
        dut = sd.CmdRx(timeout=64)

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += dut.sd_clk_rising.eq(clocker.sd_clk_rising)
        m.d.comb += dut.sd_clk_falling.eq(clocker.sd_clk_falling)

        frame = [0x08, 0x00, 0x00, 0x01, 0xaa, 0x13]

        async def card(ctx):
            ctx.set(dut.sd_cmd_i, 1)

            for _ in range(10):
                await ctx.posedge(clocker.sd_clk)

            await self._send_frame(ctx, clocker.sd_clk, dut.sd_cmd_i, frame)

        async def control(ctx):
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.half_period, 1)

            ctx.set(dut.long_response, 0)
            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            await ctx.tick().until(dut.done)

            assert ctx.get(dut.cmd_index) == 8
            assert ctx.get(dut.cmd_resp) == 0x000001aa

            assert ctx.get(dut.err_timeout) == 0
            assert ctx.get(dut.err_dir) == 0
            assert ctx.get(dut.err_crc) == 0
            assert ctx.get(dut.err_end) == 0

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(card)
            sim.add_testbench(control)

    def test_short_dir_err(self):
        clocker = sd.Clocker()
        dut = sd.CmdRx(timeout=64)

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += dut.sd_clk_rising.eq(clocker.sd_clk_rising)
        m.d.comb += dut.sd_clk_falling.eq(clocker.sd_clk_falling)

        frame = [0x48, 0x00, 0x00, 0x01, 0xaa, 0x13]

        async def card(ctx):
            ctx.set(dut.sd_cmd_i, 1)

            for _ in range(10):
                await ctx.posedge(clocker.sd_clk)

            await self._send_frame(ctx, clocker.sd_clk, dut.sd_cmd_i, frame)

        async def control(ctx):
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.half_period, 2)

            ctx.set(dut.long_response, 0)
            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            await ctx.tick().until(dut.done)

            assert ctx.get(dut.cmd_index) == 8
            assert ctx.get(dut.cmd_resp) == 0x000001aa

            assert ctx.get(dut.err_timeout) == 0
            assert ctx.get(dut.err_dir) == 1
            assert ctx.get(dut.err_crc) == 1
            assert ctx.get(dut.err_end) == 0

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(card)
            sim.add_testbench(control)

    def test_short_crc_err(self):
        clocker = sd.Clocker()
        dut = sd.CmdRx(timeout=64)

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += dut.sd_clk_rising.eq(clocker.sd_clk_rising)
        m.d.comb += dut.sd_clk_falling.eq(clocker.sd_clk_falling)

        frame = [0x08, 0x00, 0x00, 0x01, 0xaa, 0x23]

        async def card(ctx):
            ctx.set(dut.sd_cmd_i, 1)

            for _ in range(10):
                await ctx.posedge(clocker.sd_clk)

            await self._send_frame(ctx, clocker.sd_clk, dut.sd_cmd_i, frame)

        async def control(ctx):
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.half_period, 2)

            ctx.set(dut.long_response, 0)
            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            await ctx.tick().until(dut.done)

            assert ctx.get(dut.cmd_index) == 8
            assert ctx.get(dut.cmd_resp) == 0x000001aa

            assert ctx.get(dut.err_timeout) == 0
            assert ctx.get(dut.err_dir) == 0
            assert ctx.get(dut.err_crc) == 1
            assert ctx.get(dut.err_end) == 0

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(card)
            sim.add_testbench(control)

    def test_short_end_err(self):
        clocker = sd.Clocker()
        dut = sd.CmdRx(timeout=64)

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += dut.sd_clk_rising.eq(clocker.sd_clk_rising)
        m.d.comb += dut.sd_clk_falling.eq(clocker.sd_clk_falling)

        frame = [0x08, 0x00, 0x00, 0x01, 0xaa, 0x12]

        async def card(ctx):
            ctx.set(dut.sd_cmd_i, 1)

            for _ in range(10):
                await ctx.posedge(clocker.sd_clk)

            await self._send_frame(ctx, clocker.sd_clk, dut.sd_cmd_i, frame)

        async def control(ctx):
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.half_period, 2)

            ctx.set(dut.long_response, 0)
            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            await ctx.tick().until(dut.done)

            assert ctx.get(dut.cmd_index) == 8
            assert ctx.get(dut.cmd_resp) == 0x000001aa

            assert ctx.get(dut.err_timeout) == 0
            assert ctx.get(dut.err_dir) == 0
            assert ctx.get(dut.err_crc) == 0
            assert ctx.get(dut.err_end) == 1

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(card)
            sim.add_testbench(control)

    def test_long(self):
        clocker = sd.Clocker()
        dut = sd.CmdRx(timeout=64)

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += dut.sd_clk_rising.eq(clocker.sd_clk_rising)
        m.d.comb += dut.sd_clk_falling.eq(clocker.sd_clk_falling)

        frame = [0x3f, 0x03, 0x53, 0x44, 0x53, 0x55, 0x30, 0x38,
                 0x47, 0x80, 0x12, 0x34, 0x56, 0x78, 0x01, 0x86, 0xe7]

        async def card(ctx):
            ctx.set(dut.sd_cmd_i, 1)

            for _ in range(10):
                await ctx.posedge(clocker.sd_clk)

            await self._send_frame(ctx, clocker.sd_clk, dut.sd_cmd_i, frame)

        async def control(ctx):
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.half_period, 2)

            ctx.set(dut.long_response, 1)
            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            await ctx.tick().until(dut.done)

            assert ctx.get(dut.cmd_index) == 0x3f
            assert ctx.get(dut.cmd_resp) == 0x035344535530384780123456780186e7

            assert ctx.get(dut.err_timeout) == 0
            assert ctx.get(dut.err_dir) == 0
            assert ctx.get(dut.err_crc) == 0
            assert ctx.get(dut.err_end) == 0

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(card)
            sim.add_testbench(control)

    def test_long_dir_err(self):
        clocker = sd.Clocker()
        dut = sd.CmdRx(timeout=64)

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += dut.sd_clk_rising.eq(clocker.sd_clk_rising)
        m.d.comb += dut.sd_clk_falling.eq(clocker.sd_clk_falling)

        frame = [0x7f, 0x03, 0x53, 0x44, 0x53, 0x55, 0x30, 0x38,
                 0x47, 0x80, 0x12, 0x34, 0x56, 0x78, 0x01, 0x86, 0xe7]

        async def card(ctx):
            ctx.set(dut.sd_cmd_i, 1)

            for _ in range(10):
                await ctx.posedge(clocker.sd_clk)

            await self._send_frame(ctx, clocker.sd_clk, dut.sd_cmd_i, frame)

        async def control(ctx):
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.half_period, 2)

            ctx.set(dut.long_response, 1)
            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            await ctx.tick().until(dut.done)

            assert ctx.get(dut.cmd_index) == 0x3f
            assert ctx.get(dut.cmd_resp) == 0x035344535530384780123456780186e7

            assert ctx.get(dut.err_timeout) == 0
            assert ctx.get(dut.err_dir) == 1
            assert ctx.get(dut.err_crc) == 0
            assert ctx.get(dut.err_end) == 0

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(card)
            sim.add_testbench(control)

    def test_long_crc_err(self):
        clocker = sd.Clocker()
        dut = sd.CmdRx(timeout=64)

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += dut.sd_clk_rising.eq(clocker.sd_clk_rising)
        m.d.comb += dut.sd_clk_falling.eq(clocker.sd_clk_falling)

        frame = [0x3f, 0x03, 0x53, 0x44, 0x53, 0x55, 0x30, 0x38,
                 0x47, 0x80, 0x12, 0x34, 0x56, 0x78, 0x01, 0x86, 0xf7]

        async def card(ctx):
            ctx.set(dut.sd_cmd_i, 1)

            for _ in range(10):
                await ctx.posedge(clocker.sd_clk)

            await self._send_frame(ctx, clocker.sd_clk, dut.sd_cmd_i, frame)

        async def control(ctx):
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.half_period, 2)

            ctx.set(dut.long_response, 1)
            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            await ctx.tick().until(dut.done)

            assert ctx.get(dut.cmd_index) == 0x3f
            assert ctx.get(dut.cmd_resp) == 0x035344535530384780123456780186f7

            assert ctx.get(dut.err_timeout) == 0
            assert ctx.get(dut.err_dir) == 0
            assert ctx.get(dut.err_crc) == 1
            assert ctx.get(dut.err_end) == 0

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(card)
            sim.add_testbench(control)

    def test_long_end_err(self):
        clocker = sd.Clocker()
        dut = sd.CmdRx(timeout=64)

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += dut.sd_clk_rising.eq(clocker.sd_clk_rising)
        m.d.comb += dut.sd_clk_falling.eq(clocker.sd_clk_falling)

        frame = [0x3f, 0x03, 0x53, 0x44, 0x53, 0x55, 0x30, 0x38,
                 0x47, 0x80, 0x12, 0x34, 0x56, 0x78, 0x01, 0x86, 0xe6]

        async def card(ctx):
            ctx.set(dut.sd_cmd_i, 1)

            for _ in range(10):
                await ctx.posedge(clocker.sd_clk)

            await self._send_frame(ctx, clocker.sd_clk, dut.sd_cmd_i, frame)

        async def control(ctx):
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.half_period, 2)

            ctx.set(dut.long_response, 1)
            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            await ctx.tick().until(dut.done)

            assert ctx.get(dut.cmd_index) == 0x3f
            assert ctx.get(dut.cmd_resp) == 0x035344535530384780123456780186e6

            assert ctx.get(dut.err_timeout) == 0
            assert ctx.get(dut.err_dir) == 0
            assert ctx.get(dut.err_crc) == 0
            assert ctx.get(dut.err_end) == 1

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(card)
            sim.add_testbench(control)


class TestDataRx(MultiProcessTestCase):

    def _build_frame(self, data_bytes):
        block_bits = [[] for _ in range(4)]

        for byte in data_bytes:
            def put_bits(nibble):
                for i in range(4):
                    block_bits[i].append((nibble >> i) & 0x1)
            put_bits((byte >> 4) & 0xf)
            put_bits(byte & 0xf)

        crc_params = sd.CRC16_SD_DAT(data_width=1)
        crc_bits = [[] for _ in range(4)]

        for i in range(4):
            crc = crc_params.compute(block_bits[i])
            for j in reversed(range(16)):
                crc_bits[i].append((crc >> j) & 0x1)

        frame_bits = [[] for _ in range(4)]
        for i in range(4):
            frame_bits[i].append(0)
            frame_bits[i] += block_bits[i]
            frame_bits[i] += crc_bits[i]
            frame_bits[i].append(1)

        frame = []
        for nibble_bits in zip(*frame_bits):
            frame.append(sum([b << i for i, b in enumerate(nibble_bits)]))

        return frame

    async def _send_frame(self, ctx, sd_clk, sd_dat_i, frame):
        for nibble in frame:
            await ctx.negedge(sd_clk)
            ctx.set(sd_dat_i, nibble)

        await ctx.negedge(sd_clk)
        ctx.set(sd_dat_i, 0xf)

    def test_timeout(self):
        clocker = sd.Clocker()
        dut = sd.DatRx(timeout=1_000)

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += dut.sd_clk_rising.eq(clocker.sd_clk_rising)
        m.d.comb += dut.sd_clk_falling.eq(clocker.sd_clk_falling)

        async def control(ctx):
            ctx.set(dut.sd_dat_i, 0xf)
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.half_period, 2)

            ctx.set(dut.block_len, 512)
            ctx.set(dut.block_count, 1)
            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            await ctx.tick().until(dut.done)

            assert ctx.get(dut.err_timeout) == 1
            assert ctx.get(dut.err_crc) == 0
            assert ctx.get(dut.err_end) == 0

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(control)

    def test_block(self):
        clocker = sd.Clocker()
        dut = sd.DatRx(timeout=1_000)

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += dut.sd_clk_rising.eq(clocker.sd_clk_rising)
        m.d.comb += dut.sd_clk_falling.eq(clocker.sd_clk_falling)

        num_bytes = 512
        data_bytes = [i % 256 for i in range(num_bytes)]

        async def card(ctx):
            ctx.set(dut.sd_dat_i, 0xf)

            for _ in range(10):
                await ctx.posedge(clocker.sd_clk)

            frame = self._build_frame(data_bytes)
            await self._send_frame(ctx, clocker.sd_clk, dut.sd_dat_i, frame)

        async def control(ctx):
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.half_period, 2)

            ctx.set(dut.block_len, num_bytes)
            ctx.set(dut.block_count, 1)
            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            await ctx.tick().until(dut.done)

            assert ctx.get(dut.err_timeout) == 0
            assert ctx.get(dut.err_crc) == 0
            assert ctx.get(dut.err_end) == 0

        async def stream(ctx):
            recv_bytes = []
            for _ in range(num_bytes):
                payload, = await ctx.tick().sample(dut.source.payload).until(dut.source.valid)
                recv_bytes.append(payload)

            assert recv_bytes == data_bytes

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(card)
            sim.add_testbench(control)
            sim.add_testbench(stream)

    def test_block_min_half_period(self):
        clocker = sd.Clocker()
        dut = sd.DatRx(timeout=1_000)

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += dut.sd_clk_rising.eq(clocker.sd_clk_rising)
        m.d.comb += dut.sd_clk_falling.eq(clocker.sd_clk_falling)

        num_bytes = 512
        data_bytes = [i % 256 for i in range(num_bytes)]

        async def card(ctx):
            ctx.set(dut.sd_dat_i, 0xf)

            for _ in range(10):
                await ctx.posedge(clocker.sd_clk)

            frame = self._build_frame(data_bytes)
            await self._send_frame(ctx, clocker.sd_clk, dut.sd_dat_i, frame)

        async def control(ctx):
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.half_period, 1)

            ctx.set(dut.block_len, num_bytes)
            ctx.set(dut.block_count, 1)
            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            await ctx.tick().until(dut.done)

            assert ctx.get(dut.err_timeout) == 0
            assert ctx.get(dut.err_crc) == 0
            assert ctx.get(dut.err_end) == 0

        async def stream(ctx):
            recv_bytes = []
            for _ in range(num_bytes):
                payload, = await ctx.tick().sample(dut.source.payload).until(dut.source.valid)
                recv_bytes.append(payload)

            assert recv_bytes == data_bytes

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(card)
            sim.add_testbench(control)
            sim.add_testbench(stream)

    def test_block_crc_err(self):
        clocker = sd.Clocker()
        dut = sd.DatRx(timeout=1_000)

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += dut.sd_clk_rising.eq(clocker.sd_clk_rising)
        m.d.comb += dut.sd_clk_falling.eq(clocker.sd_clk_falling)

        num_bytes = 512
        data_bytes = [i % 256 for i in range(num_bytes)]

        async def card(ctx):
            ctx.set(dut.sd_dat_i, 0xf)

            for _ in range(10):
                await ctx.posedge(clocker.sd_clk)

            frame = self._build_frame(data_bytes)
            frame[-2] ^= 0x1

            await self._send_frame(ctx, clocker.sd_clk, dut.sd_dat_i, frame)

        async def control(ctx):
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.half_period, 2)

            ctx.set(dut.block_len, num_bytes)
            ctx.set(dut.block_count, 1)
            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            await ctx.tick().until(dut.done)

            assert ctx.get(dut.err_timeout) == 0
            assert ctx.get(dut.err_crc) == 1
            assert ctx.get(dut.err_end) == 0

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(card)
            sim.add_testbench(control)

    def test_block_end_err(self):
        clocker = sd.Clocker()
        dut = sd.DatRx(timeout=1_000)

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += dut.sd_clk_rising.eq(clocker.sd_clk_rising)
        m.d.comb += dut.sd_clk_falling.eq(clocker.sd_clk_falling)

        num_bytes = 512
        data_bytes = [i % 256 for i in range(num_bytes)]

        async def card(ctx):
            ctx.set(dut.sd_dat_i, 0xf)

            for _ in range(10):
                await ctx.posedge(clocker.sd_clk)

            frame = self._build_frame(data_bytes)
            frame[-1] ^= 0x1

            await self._send_frame(ctx, clocker.sd_clk, dut.sd_dat_i, frame)

        async def control(ctx):
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.half_period, 2)

            ctx.set(dut.block_len, num_bytes)
            ctx.set(dut.block_count, 1)
            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            await ctx.tick().until(dut.done)

            assert ctx.get(dut.err_timeout) == 0
            assert ctx.get(dut.err_crc) == 0
            assert ctx.get(dut.err_end) == 1

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(card)
            sim.add_testbench(control)

    def test_multi_block(self):
        clocker = sd.Clocker()
        dut = sd.DatRx(timeout=1_000)

        m = Module()
        m.submodules.clocker = clocker
        m.submodules.dut = dut

        m.d.comb += dut.sd_clk_rising.eq(clocker.sd_clk_rising)
        m.d.comb += dut.sd_clk_falling.eq(clocker.sd_clk_falling)

        num_blocks = 2
        num_bytes = 512

        blocks = []
        for i in range(num_blocks):
            blocks.append([(j * (i + 1)) % 256 for j in range(num_bytes)])

        async def card(ctx):
            ctx.set(dut.sd_dat_i, 0xf)

            for _ in range(10):
                await ctx.posedge(clocker.sd_clk)

            for data_bytes in blocks:
                frame = self._build_frame(data_bytes)
                await self._send_frame(ctx, clocker.sd_clk, dut.sd_dat_i, frame)

        async def control(ctx):
            ctx.set(clocker.enable, 1)
            ctx.set(clocker.half_period, 2)

            ctx.set(dut.block_len, num_bytes)
            ctx.set(dut.block_count, num_blocks)
            ctx.set(dut.start, 1)

            await ctx.tick()
            ctx.set(dut.start, 0)

            await ctx.tick().until(dut.done)

            assert ctx.get(dut.err_timeout) == 0
            assert ctx.get(dut.err_crc) == 0
            assert ctx.get(dut.err_end) == 0

        async def stream(ctx):
            recv_blocks = []
            for _ in range(num_blocks):
                recv_bytes = []
                for _ in range(num_bytes):
                    payload, = await ctx.tick().sample(dut.source.payload).until(dut.source.valid)
                    recv_bytes.append(payload)
                recv_blocks.append(recv_bytes)

            assert recv_blocks == blocks

        with self.simulate(m) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(card)
            sim.add_testbench(control)
            sim.add_testbench(stream)


class TestSDSequencer(MultiProcessTestCase):

    def test_basic(self):
        config = sd.ControllerConfig(clk_freq=40e6)
        ctrlr = sd.Controller(config=config)
        dut = sd.Sequencer(ctrlr=ctrlr)

        m = Module()
        m.submodules.ctrlr = ctrlr
        m.submodules.dut = dut

        async def testbench(ctx):
            ctx.set(ctrlr.bus.cmd.i, 1)

            await ctx.tick().repeat(10000)

        traces = [
            ctrlr.bus,
        ]

        with self.simulate(m, traces=traces) as sim:
            sim.add_clock(1.0 / 100e6)
            sim.add_testbench(testbench)
