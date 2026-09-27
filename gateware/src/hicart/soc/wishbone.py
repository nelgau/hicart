from dataclasses import dataclass

from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth.utils import exact_log2
from amaranth_soc.memory import MemoryMap
from amaranth_soc import wishbone


class WindowMapper(wiring.Component):

    def __init__(self, sub_bus, *, addr_width, base_addr, name="mapped window"):
        if addr_width > sub_bus.addr_width:
            raise ValueError("Window mapper bus cannot be wider than subordinate bus")

        granularity_bits = exact_log2(sub_bus.data_width // sub_bus.granularity)
        effective_addr_width = addr_width + granularity_bits

        if base_addr & ((1 << effective_addr_width) - 1) != 0:
            raise ValueError("Window mapper bus cannot overlap base address")

        self.sub_bus = sub_bus
        self.base_addr = base_addr
        self._base_pattern = Const(self.base_addr >> effective_addr_width)

        # FIXME: It would be possible to implement this so that the resources
        # on the subordinate bus are visible, removing the need to create this
        # hacky placeholder resource. Unfortunately, because it's possible to
        # slice a resource using a window mapper, we'd need a way to represent
        # a subset of a resource and that doesn't seem trivial to do.
        map_addr_width = max(1, effective_addr_width)
        memory_map = MemoryMap(addr_width=map_addr_width, data_width=sub_bus.granularity)
        memory_map.add_resource(self, size=2**addr_width, name=name)

        bus_signature = wishbone.Signature(
            addr_width=addr_width,
            data_width=sub_bus.data_width,
            granularity=sub_bus.granularity,
            features=sub_bus.features)

        super().__init__({
            "bus": In(bus_signature)
        })
        self.bus.memory_map = memory_map

    def elaborate(self, platform):
        m = Module()

        m.d.comb += [
            self.sub_bus.adr    .eq(Cat(self.bus.adr, self._base_pattern)),

            self.sub_bus.dat_w  .eq(self.bus.dat_w),
            self.sub_bus.sel    .eq(self.bus.sel),
            self.sub_bus.cyc    .eq(self.bus.cyc),
            self.sub_bus.stb    .eq(self.bus.stb),
            self.sub_bus.we     .eq(self.bus.we),

            self.bus.dat_r      .eq(self.sub_bus.dat_r),
            self.bus.ack        .eq(self.sub_bus.ack),
        ]

        if hasattr(self.bus, "lock"):
            m.d.comb += self.sub_bus.lock.eq(self.bus.lock)
        if hasattr(self.bus, "cti"):
            m.d.comb += self.sub_bus.cti.eq(self.bus.cti)
        if hasattr(self.bus, "bte"):
            m.d.comb += self.sub_bus.bte.eq(self.bus.bte)
        if hasattr(self.bus, "err"):
            m.d.comb += self.bus.err.eq(self.sub_bus.err)
        if hasattr(self.bus, "rty"):
            m.d.comb += self.bus.rty.eq(self.sub_bus.rty)
        if hasattr(self.bus, "stall"):
            m.d.comb += self.bus.stall.eq(self.sub_bus.stall)

        return m


class WishboneFeatureShim(wiring.Component):
    """A connector for Wishbone bus interfaces with mismatching features.

    This class was borrowed from Amaranth's SOC library, where it's private.
    """
    def __init__(self, addr_width, data_width, granularity=None, intr_features=frozenset(),
                 sub_features=frozenset()):
        super().__init__({
            "intr_bus": In(wishbone.Signature(addr_width=addr_width, data_width=data_width,
                                     granularity=granularity, features=intr_features)),
            "sub_bus": Out(wishbone.Signature(addr_width=addr_width, data_width=data_width,
                                     granularity=granularity, features=sub_features))})

    def elaborate(self, platform):
        m = Module()

        m.d.comb += [
            self.sub_bus.cyc.eq(self.intr_bus.cyc),
            self.sub_bus.stb.eq(self.intr_bus.stb),
            self.sub_bus.adr.eq(self.intr_bus.adr),
            self.sub_bus.sel.eq(self.intr_bus.sel),
            self.sub_bus.we.eq(self.intr_bus.we),
            self.sub_bus.dat_w.eq(self.intr_bus.dat_w),
            self.intr_bus.dat_r.eq(self.sub_bus.dat_r)
        ]
        if hasattr(self.sub_bus, "lock"):
            m.d.comb += self.sub_bus.lock.eq(getattr(self.intr_bus, "lock", self.intr_bus.cyc))
        if hasattr(self.sub_bus, "cti"):
            m.d.comb += self.sub_bus.cti.eq(getattr(self.intr_bus, "cti", wishbone.CycleType.CLASSIC))
        if hasattr(self.sub_bus, "bte"):
            m.d.comb += self.sub_bus.bte.eq(getattr(self.intr_bus, "bte", wishbone.BurstTypeExt.LINEAR))
        if hasattr(self.intr_bus, "err"):
            m.d.comb += self.intr_bus.err.eq(getattr(self.sub_bus, "err", 0))
        if hasattr(self.intr_bus, "rty"):
            m.d.comb += self.intr_bus.rty.eq(getattr(self.sub_bus, "rty", 0))

        # If the initiator doesn't have ERR or RTY, connect them to ACK.
        intr_ack_fanin = self.sub_bus.ack
        if hasattr(self.sub_bus, "err") and not hasattr(self.intr_bus, "err"):
            intr_ack_fanin |= self.sub_bus.err
        if hasattr(self.sub_bus, "rty") and not hasattr(self.intr_bus, "rty"):
            intr_ack_fanin |= self.sub_bus.rty
        m.d.comb += self.intr_bus.ack.eq(intr_ack_fanin)

        sub_ack_err_rty = self.sub_bus.ack \
                        | getattr(self.sub_bus, "err", 0) \
                        | getattr(self.sub_bus, "rty", 0)

        if hasattr(self.intr_bus, "stall") and hasattr(self.sub_bus, "stall"):
            # Pipelined initiator to pipelined subordinate.
            m.d.comb += self.intr_bus.stall.eq(self.sub_bus.stall)
        elif hasattr(self.intr_bus, "stall"):
            # Pipelined initiator to standard subordinate.
            m.d.comb += self.intr_bus.stall.eq(self.intr_bus.cyc & ~sub_ack_err_rty)
        elif hasattr(self.sub_bus, "stall"):
            # Standard initiator to pipelined subordinate.
            # In pipelined mode, a new transfer is initiated every clock cycle where STB is high
            # and STALL is low. To accomodate a standard mode initiator, STB is limited to a one-
            # clock pulse until the subordinate asserts ACK, ERR or RTY.
            with m.FSM():
                with m.State("IDLE"):
                    m.d.comb += self.sub_bus.stb.eq(self.intr_bus.stb)
                    with m.If(self.intr_bus.cyc & self.intr_bus.stb & ~self.sub_bus.stall):
                        m.next = "BUSY"
                with m.State("BUSY"):
                    m.d.comb += self.sub_bus.stb.eq(0)
                    with m.If(~self.intr_bus.cyc | sub_ack_err_rty):
                        m.next = "IDLE"

        return m


class WishbonePipelinedDriver:

    def __init__(self, bus):
        self.bus = bus

    async def begin(self, ctx):
        pass

    async def read_once(self, ctx, address):
        ctx.set(self.bus.cyc, 1)
        ctx.set(self.bus.we, 0)

        ctx.set(self.bus.stb, 1)
        ctx.set(self.bus.adr, address)

        while ctx.get(self.bus.stall):
            await ctx.tick()

        await ctx.tick()

        ctx.set(self.bus.stb, 0)

        while not ctx.get(self.bus.ack):
            await ctx.tick()

        result = ctx.get(self.bus.dat_r)
        await ctx.tick()

        ctx.set(self.bus.cyc, 0)
        await ctx.tick()

        return result

    async def read_sequential(self, ctx, start_address, count, stride=1):
        address = start_address
        stb_count = 0
        ack_count = 0
        result = []

        ctx.set(self.bus.cyc, 1)
        ctx.set(self.bus.we, 0)

        while ack_count < count:
            if stb_count < count:
                ctx.set(self.bus.adr, address)
                ctx.set(self.bus.stb, 1)

                if not ctx.get(self.bus.stall):
                    address += stride
                    stb_count += 1
            else:
                ctx.set(self.bus.stb, 0)
                ctx.set(self.bus.adr, 0)

            if ctx.get(self.bus.ack):
                result.append(ctx.get(self.bus.dat_r))
                ack_count += 1

            await ctx.tick()

        ctx.set(self.bus.cyc, 0)
        await ctx.tick()

        return result


class WishbonePipelinedResponder:

    @dataclass
    class _Task:
        address: int
        is_write: bool
        write_data: int

    def __init__(self, bus, *, initial=0, delay=0, max_outstanding=None):
        if delay < 0:
            raise ValueError(f"Delay must be non-negative")
        if max_outstanding is not None and max_outstanding < 1:
            raise ValueError(f"Max outstanding must be None or positive")

        self.bus = bus

        self.delay = delay
        self.max_outstanding = max_outstanding

        self.counter = initial
        self.stalled = False

        self._reset_pipeline()

    async def run(self, ctx):
        ctx.set(self.bus.ack, 0)
        ctx.set(self.bus.dat_r, 0)
        ctx.set(self.bus.stall, 0)

        async for _, rst_active, cyc, stb, adr, we, dat_w in (
            ctx.tick().sample(
                self.bus.cyc,
                self.bus.stb,
                self.bus.adr,
                self.bus.we,
                self.bus.dat_w,
            )
        ):
            result = 0
            ack = False

            if rst_active or not cyc:
                self._reset_pipeline()
            else:
                new_task = None
                if cyc & stb and not self.stalled:
                    new_task = self._Task(adr, we, dat_w)

                self.pipeline.append(new_task)
                curr_task = self.pipeline.pop(0)

                if curr_task is not None:
                    result = self._dispatch_task(curr_task)
                    ack = True

            if self.max_outstanding is not None:
                self.stalled = self.num_accepted_tasks >= self.max_outstanding

            ctx.set(self.bus.ack, ack)
            ctx.set(self.bus.stall, self.stalled)
            ctx.set(self.bus.dat_r, result)

    @property
    def num_accepted_tasks(self):
        return sum(t is not None for t in self.pipeline)

    def _reset_pipeline(self):
        self.pipeline = [None for _ in range(self.delay)]

    def _dispatch_task(self, task):
        if task.is_write:
            return 0
        else:
            result = self.counter
            self.counter += 1
            return result
