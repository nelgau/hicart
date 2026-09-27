from amaranth import *
from amaranth.hdl.rec import DIR_FANIN, DIR_FANOUT


class BasicStream(Record):

    def __init__(self, width):
        super().__init__([
            ('payload',     width,  DIR_FANOUT),
            ('valid',       1,      DIR_FANOUT),
            ('ready',       1,      DIR_FANIN)
        ])


class ByteDownConverter(Elaboratable):

    def __init__(self, byte_width):
        self.byte_width = byte_width

        self.source = BasicStream(width=8 * byte_width)
        self.sink   = BasicStream(width=8)

    def elaborate(self, platform):
        m = Module()

        data_shift = Signal.like(self.source.payload)
        bytes_to_send = Signal(range(0, self.byte_width + 1))

        m.d.comb += [
            self.sink.payload.eq(data_shift[0:8])
        ]

        with m.FSM():

            with m.State("IDLE"):
                m.d.comb += self.source.ready.eq(1)

                # Once we get a send request, fill in our shift register, and start shifting.
                with m.If(self.source.valid):
                    m.d.sync += [
                        data_shift         .eq(self.source.payload),
                        bytes_to_send      .eq(self.byte_width - 1),
                    ]
                    m.next = "RUN"

            with m.State("RUN"):
                m.d.comb += self.sink.valid.eq(1)

                # Once the UART is accepting our input...
                with m.If(self.sink.ready):

                    # ... if we have bytes left to send, move to the next one.
                    with m.If(bytes_to_send > 0):
                        m.d.sync += [
                            bytes_to_send .eq(bytes_to_send - 1),
                            data_shift    .eq(data_shift[8:]),
                        ]

                    # Otherwise, complete the frame.
                    with m.Else():
                        m.d.comb += self.source.ready.eq(1)

                        # If we still have data to send, move to the next byte...
                        with m.If(self.source.valid):
                            m.d.sync += [
                                bytes_to_send      .eq(self.byte_width - 1),
                                data_shift         .eq(self.source.payload),
                            ]

                        # ... otherwise, move to our idle state.
                        with m.Else():
                            m.next = "IDLE"

        return m


class StreamDriver:

    def __init__(self, stream):
        self.stream = stream

    async def begin(self, ctx):
        pass

    async def produce(self, ctx, items):
        ctx.set(self.stream.valid, 1)

        for item in items:
            ctx.set(self.stream.payload, item)

            while not ctx.get(self.stream.ready):
                await ctx.tick()

            await ctx.tick()

        ctx.set(self.stream.payload, 0)
        ctx.set(self.stream.valid, 0)

    async def consume(self, ctx, count=1):
        results = []

        ctx.set(self.stream.ready, 1)

        while len(results) < count:
            while not ctx.get(self.stream.valid):
                await ctx.tick()

            results.append(ctx.get(self.stream.payload))
            await ctx.tick()

        ctx.set(self.stream.ready, 0)

        return results
