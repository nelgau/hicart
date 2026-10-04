from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth.utils import exact_log2
from amaranth_soc import wishbone
from amaranth_soc.memory import MemoryMap


FlashSignature = wiring.Signature({
    "cs_n": Out(1, init=1),
    "sck_en": Out(1),
    "d": Out(wiring.Signature({
        "i":    In(4),
        "o":    Out(4),
        "oe":   Out(4),
    }))
})


QSPISignature = wiring.Signature({
    "cs_n": Out(1, init=1),
    "sck": Out(1),
    "d": Out(wiring.Signature({
        "i":    In(4),
        "o":    Out(4),
        "oe":   Out(4),
    }))
})


class SimFlashIO(wiring.Component):
    bus: In(FlashSignature)
    port: Out(QSPISignature)

    def elaborate(self, platform):
        m = Module()

        m.domains.sync_neg = sync_neg = ClockDomain()
        m.d.comb += sync_neg.clk.eq(~ClockSignal())

        m.d.comb += [
            self.port.cs_n  .eq(self.bus.cs_n),
            self.port.sck   .eq(self.bus.sck_en & sync_neg.clk),

            self.port.d.o   .eq(self.bus.d.o),
            self.port.d.oe  .eq(self.bus.d.oe),

            self.bus.d.i    .eq(self.port.d.i),
        ]

        return m


class FlashController(wiring.Component):

    def __init__(self, *, data_width=8, byteorder="little"):
        if data_width % 8 != 0:
            raise ValueError("Data width must be a multiple of eight")
        if byteorder not in ("little", "big"):
            raise ValueError("Byte order must be either little or big")
        if byteorder == "little":
            raise NotImplementedError

        self.granularity_bits = exact_log2(data_width // 8)
        self.addr_width = 24 - self.granularity_bits
        self.data_width = data_width

        super().__init__({
            "bus":      Out(FlashSignature),

            "start":    In(1),
            "address":  In(self.addr_width),
            "idle":     Out(1),
            "valid":    Out(1),
            "data":     Out(data_width),
        })

        self._in_shift      = Signal(data_width)
        self._out_shift     = Signal(80)
        self._oe_shift      = Signal(80)

        self._counter       = Signal(5)
        self._data_counter  = Signal(range(data_width // 4))

    def elaborate(self, platform):
        m = Module()

        m.d.sync += [
            self._in_shift[4:]      .eq(self._in_shift[:-4]),
            self._in_shift[:4]      .eq(self.bus.d.i),

            self._out_shift[4:]     .eq(self._out_shift[:-4]),
            self._out_shift[:4]     .eq(0),

            self._oe_shift[4:]      .eq(self._oe_shift[:-4]),
            self._oe_shift[:4]      .eq(0),

            self.valid              .eq(0),
        ]

        m.d.comb += [
            self.bus.d.o            .eq(self._out_shift[-4:]),
            self.bus.d.oe           .eq(self._oe_shift[-4:]),

            self.data               .eq(self._in_shift),
            self.idle               .eq(0),
        ]

        with m.If(self._counter != 0):
            m.d.sync += self._counter.eq(self._counter - 1)
        with m.If(self._data_counter != 0):
            m.d.sync += self._data_counter.eq(self._data_counter - 1)


        request_address = Cat(C(0, self.granularity_bits), self.address)
        current_address = Signal(24)

        with m.FSM():

            with m.State("INITIAL"):
                m.next = "STARTUP"
                m.d.sync += self._counter       .eq(7)

            with m.State("STARTUP"):
                with m.If(self._counter == 0):
                    m.next = "IDLE"

            with m.State("IDLE"):
                m.d.comb += self.idle           .eq(1)

                with m.If(self.start):
                    m.next = "START"
                    m.d.sync += [
                        current_address         .eq(request_address),
                    ]

            with m.State("START"):
                m.next = "SEND"
                m.d.sync += [
                    self._counter               .eq(19),
                    self.bus.cs_n               .eq(0),
                    self.bus.sck_en             .eq(1),

                    self._out_shift[48:80]      .eq(0x11101011),
                    self._oe_shift[48:80]       .eq(0x11111111),

                    self._out_shift[24:48]      .eq(current_address),
                    self._oe_shift[24:48]       .eq(0xFFFFFF),

                    self._out_shift[16:24]      .eq(0xF0),
                    self._oe_shift[16:24]       .eq(0xFF),

                    self._out_shift[0:16]       .eq(0x0000),
                    self._oe_shift[0:16]        .eq(0x0000),
                ]

            with m.State("SEND"):
                with m.If(self._counter == 0):
                    m.next = "DATA"
                    m.d.sync += [
                        self._data_counter      .eq(self.data_width // 4 - 1),
                    ]

            with m.State("DATA"):
                with m.If(self._data_counter & 0x1 == 0):
                    m.d.sync += [
                        current_address         .eq(current_address + 1)
                    ]

                with m.If(self._data_counter == 0):
                    m.next = "WAITING"
                    m.d.sync += [
                        self.valid              .eq(1),
                        self.bus.sck_en         .eq(0),
                    ]

            with m.State("WAITING"):
                m.d.comb += self.idle           .eq(1)

                with m.If(self.start):
                    with m.If(current_address == request_address):
                        m.next = "DATA"
                        m.d.sync += [
                            self._data_counter  .eq(self.data_width // 4 - 1),
                            self.bus.sck_en     .eq(1),
                        ]
                    with m.Else():
                        m.next = "RECOVERY"
                        m.d.sync += [
                            current_address     .eq(request_address),
                            self._counter       .eq(7),
                            self.bus.cs_n       .eq(1),
                        ]

            with m.State("RECOVERY"):
                with m.If(self._counter == 0):
                    m.next = "START"

        return m


class WishboneFlashController(wiring.Component):

    def __init__(self, data_width=8, byteorder="little"):
        if data_width % 8 != 0:
            raise ValueError("Data width must be a multiple of eight")
        if byteorder not in ("little", "big"):
            raise ValueError("Byte order must be either little or big")
        if byteorder == "little":
            raise NotImplementedError

        self._byteorder = byteorder

        granularity_bits = exact_log2(data_width // 8)
        addr_width = 24 - granularity_bits

        wb_signature = wishbone.Signature(
            addr_width=addr_width,
            data_width=data_width,
            granularity=8,
            features={"stall"})

        super().__init__({
            "bus":  Out(FlashSignature),
            "wb":   In(wb_signature),
        })
        self.wb.memory_map = MemoryMap(addr_width=24, data_width=8)
        self.wb.memory_map.add_resource(self, size=2**24, name="flash")
        self.wb.memory_map.freeze()

    def elaborate(self, platform):
        m = Module()

        m.submodules.inner = inner = FlashController(
            data_width=self.wb.data_width,
            byteorder=self._byteorder,
        )

        wiring.connect(m, inner.bus, wiring.flipped(self.bus))

        m.d.comb += [
            inner.start     .eq(self.wb.cyc & self.wb.stb),
            inner.address   .eq(self.wb.adr),

            self.wb.stall   .eq(~inner.idle),
            self.wb.dat_r   .eq(inner.data),
            self.wb.ack     .eq(inner.valid),
        ]

        return m


class FlashResponder:

    def __init__(self, qspi, data):
        self.qspi = qspi
        self.data = data

    async def run(self, ctx):
        while True:
            await self._wait_for_cs(ctx)

            command = await self._read_spi(ctx, 8)
            if command is None:
                continue

            assert command == 0xEB

            address = await self._read_qspi(ctx, 6)
            if address is None:
                continue

            mode = await self._read_qspi(ctx, 2)
            if mode is None:
                continue

            assert mode == 0xF0

            dummy = await self._read_qspi(ctx, 4)
            if dummy is None:
                continue

            while True:
                data = self._load_data(address)
                bursting = await self._write_qspi(ctx, 2, data)
                if not bursting:
                    break
                address += 1

    def _load_data(self, address):
        if address < len(self.data):
            return self.data[address]
        else:
            return 0xFF

    async def _read_spi(self, ctx, bit_count):
        result = 0

        for i in range(bit_count):
            aborted, qspi_do = await self._wait_for_read_clock(ctx)
            if aborted:
                return None

            result = (result << 1) | (qspi_do & 0x1)

        return result

    async def _read_qspi(self, ctx, nibble_count):
        result = 0

        for i in range(nibble_count):
            aborted, qspi_do = await self._wait_for_read_clock(ctx)
            if aborted:
                return None

            result = (result << 4) | (qspi_do & 0xF)

        return result

    async def _write_qspi(self, ctx, nibble_count, data):
        nibbles = []
        for i in range(nibble_count):
            nibbles.append(data & 0xF)
            data >>= 4

        for nibble in reversed(nibbles):
            aborted = await self._wait_for_write_clock(ctx)
            if aborted:
                return False

            ctx.set(self.qspi.d.i, nibble)

        return True

    async def _wait_for_cs(self, ctx):
        await ctx.negedge(self.qspi.cs_n)

    async def _wait_for_read_clock(self, ctx):
        cs_n, _, qspi_do = await (
            ctx.posedge(self.qspi.cs_n)
                    .posedge(self.qspi.sck)
                    .sample(self.qspi.d.o)
        )
        return (cs_n == 1, qspi_do)

    async def _wait_for_write_clock(self, ctx):
        cs_n, _ = await (
            ctx.posedge(self.qspi.cs_n)
                    .negedge(self.qspi.sck)
        )
        return (cs_n == 1)
