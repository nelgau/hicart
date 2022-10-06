from amaranth import *
from amaranth.sim import *
from amaranth.utils import log2_int
from amaranth_soc.memory import MemoryMap
from amaranth_soc.wishbone import Interface

from hicart.test.testcase import MultiProcessTestCase
from hicart.test.driver.wishbone import WishboneInitiator
from hicart.test.emulator.wishbone import WishboneEmulator


class DownConverter(Elaboratable):

    def __init__(self, *, sub_bus, addr_width, data_width, granularity=None, features=frozenset()):
        if granularity is None:
            granularity  = data_width

        self.sub_bus = sub_bus

        self.addr_width  = addr_width
        self.data_width  = data_width
        self.granularity = granularity
        self.features    = set(features)

        self.bus = Interface(addr_width=addr_width, data_width=data_width,
            granularity=granularity, features=features)

        granularity_bits = log2_int(data_width // granularity)
        memory_map = MemoryMap(addr_width=max(1, addr_width + granularity_bits),
                               data_width=granularity)
        memory_map.add_window(sub_bus.memory_map)
        self.bus.memory_map = memory_map

    def elaborate(self, platform):
        m = Module()

        dw_from = len(self.bus.dat_w)
        dw_to   = len(self.sub_bus.dat_w)
        ratio   = dw_from // dw_to

        stb_counter = Signal(range(ratio))
        ack_counter = Signal(range(ratio))

        #
        # Control Path
        #

        # State Machine

        with m.FSM() as fsm:

            m.d.comb += [
                self.bus.stall.eq(~fsm.ongoing("IDLE") & ~self.bus.ack),                
            ]

            with m.State("IDLE"):
                with m.If(self.bus.cyc & self.bus.stb):
                    m.next = "SENDING"

            with m.State("SENDING"):
                m.d.comb += self.sub_bus.cyc.eq(1)
                m.d.comb += self.sub_bus.stb.eq(1)

                with m.If(~self.sub_bus.stall):

                    with m.If(stb_counter == (ratio - 1)):
                        m.next = "WAITING"

            with m.State("WAITING"):
                m.d.comb += self.sub_bus.cyc.eq(1)

                with m.If(self.sub_bus.ack):
                    with m.If(ack_counter == (ratio - 1)):
                        m.d.comb += self.bus.ack.eq(1)

                        m.next = "IDLE"

                        with m.If(self.bus.cyc & self.bus.stb):
                            m.next = "SENDING"                

        # Strobe/Ack Counters

        with m.If(self.sub_bus.cyc & self.sub_bus.stb & ~self.sub_bus.stall):
            m.d.sync += stb_counter.eq(stb_counter + 1)

        with m.If(self.sub_bus.ack):
            m.d.sync += ack_counter.eq(ack_counter + 1)

        with m.If(self.bus.cyc & self.bus.stb & ~self.bus.stall):
            m.d.sync += stb_counter.eq(0)
            m.d.sync += ack_counter.eq(0)

        #
        # Data Path
        #

        # Address

        address = Signal(self.addr_width, reset_less=True)

        with m.If(self.bus.cyc & self.bus.stb & ~self.bus.stall):
            m.d.sync += address.eq(self.bus.adr)

        m.d.comb += self.sub_bus.adr.eq(Cat(stb_counter, address))            

        # Write

        m.d.comb += self.sub_bus.dat_w.eq(self.bus.word_select(stb_counter, dw_to))

        # Read

        dat_r = Signal(dw_from, reset_less=True)

        # m.d.comb += self.bus.dat_r.eq(Cat(dat_r[dw_to:], self.sub_bus.dat_r))          # Little Endian
        m.d.comb += self.bus.dat_r.eq(Cat(self.sub_bus.dat_r, dat_r[:dw_from - dw_to]))    # Big Endian

        with m.If(self.sub_bus.ack):
            m.d.sync += dat_r.eq(self.bus.dat_r)

        return m

    def ports(self):
        return [
            self.bus,
            self.sub_bus
        ]

class Translator(Elaboratable):
    """Bus Translator

    A resource for accessing a range of addresses on a subordinate bus.
    """
    def __init__(self, *, sub_bus, base_addr, addr_width, features=frozenset()):
        self.sub_bus = sub_bus
        self.base_addr = base_addr

        self.bus = Interface(addr_width=addr_width,
                             data_width=sub_bus.data_width,
                             granularity=sub_bus.granularity,
                             features=features)

        # FIXME: It would be possible to implement this so that the resources
        # on the subordinate bus are visible, removing the need to create this
        # hacky placeholder resource. Unfortunately, because it's possible to
        # slice a resource using a translator, we'd need a way to represent
        # a subset of a resource and that doesn't seem trivial to do.
        memory_map = MemoryMap(addr_width=addr_width, data_width=sub_bus.data_width)
        memory_map.add_resource(self, size=2**addr_width, name='translator')
        self.bus.memory_map = memory_map

    def elaborate(self, platform):
        m = Module()

        # If the result of the addition is automatically extended to the width
        # of the subordinate bus, this auxiliary signal is unnecessary.
        adr_extended = Signal.like(self.sub_bus.adr)

        m.d.comb += [
            self.bus            .connect(self.sub_bus, exclude={"adr"}),

            adr_extended        .eq(self.bus.adr),
            self.sub_bus.adr    .eq(adr_extended + self.base_addr),
        ]

        return m

class DownConverterTest(MultiProcessTestCase):

    def test_simple(self):
        sub_bus = Interface(addr_width=24, data_width=8, features={"stall"})
        sub_bus.memory_map = MemoryMap(addr_width=24, data_width=8)

        dut = DownConverter(sub_bus=sub_bus, addr_width=22, data_width=32,
            granularity=8, features={"stall"})

        intr_driver = WishboneInitiator(dut.bus)
        sub_emulator = WishboneEmulator(sub_bus, delay=1, max_outstanding=1)

        def intr_process():
            yield from intr_driver.begin()
            yield from intr_driver.read_sequential(5, 0x00040000, 7)

        def sub_process():
            yield Passive()
            yield from sub_emulator.emulate()

        with self.simulate(dut, traces=dut.ports()) as sim:
            sim.add_clock(1.0 / 100e6, domain='sync')
            sim.add_sync_process(intr_process)
            sim.add_sync_process(sub_process)        
