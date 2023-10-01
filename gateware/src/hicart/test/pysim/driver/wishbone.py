from amaranth.sim import *


class WishboneInitiatorDriver:

    def __init__(self, bus):
        self.bus = bus

    def begin(self):
        yield

    def read_once(self, address):
        yield self.bus.cyc.eq(1)
        yield self.bus.we.eq(0)

        yield self.bus.stb.eq(1)
        yield self.bus.adr.eq(address)

        while (yield self.bus.stall):
            yield

        yield

        yield self.bus.stb.eq(0)
        
        while not (yield self.bus.ack):
            yield

        result = (yield self.bus.dat_r)

        yield self.bus.cyc.eq(0)
        yield

        return result

    def read_sequential(self, count, start_address, stride):
        address = start_address
        stb_count = 0
        ack_count = 0
        cycles = 0
        result = []

        yield self.bus.cyc.eq(1)
        yield self.bus.we.eq(0)

        while ack_count < count:
            yield Settle()

            if stb_count < count:
                yield self.bus.stb.eq(1)
                yield self.bus.adr.eq(address)

                if (yield self.bus.stall) == 0:
                    address += stride
                    stb_count += 1
            else:
                yield self.bus.stb.eq(0)
                yield self.bus.adr.eq(0)

            if (yield self.bus.ack):
                result.append((yield self.bus.dat_r))
                ack_count += 1

            yield

            cycles += 1
            if cycles > 100:
                return None

        yield self.bus.cyc.eq(0)
        yield

        return result
