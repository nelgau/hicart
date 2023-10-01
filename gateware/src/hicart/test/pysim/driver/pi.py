from amaranth.sim import *

# N.B. The control signals (e.g., ale_l, ale_h, read, write) need to be inverted!

class PIInitiatorDriver:

    def __init__(self, pi):
        self.pi = pi

    def begin(self):
        yield self.pi.ale_l.eq(1)
        yield self.pi.ale_h.eq(0)
        yield Delay(1e-6)

    def read_burst_slow(self, start_address, word_count):
        yield self.pi.ale_l.eq(0)
        yield Delay(56e-9)
        yield self.pi.ad.i.eq((start_address >> 16) & 0xFFFF)
        yield Delay(56e-9)
        yield self.pi.ale_h.eq(1)
        yield Delay(56e-9)
        yield self.pi.ad.i.eq(start_address & 0xFFFF)
        yield Delay(56e-9)
        yield self.pi.ale_l.eq(1)
        yield Delay(1040e-9)

        address = start_address
        result = []

        for i in range(word_count):
            yield self.pi.read.eq(1)
            yield Delay(304e-9)

            word = yield self.pi.ad.o
            yield self.pi.read.eq(0)
            yield Delay(64e-9)

            result.append((address, word))
            address += 2

        yield self.pi.ale_h.eq(0)
        yield Delay(2256e-9)

        return result

    def read_burst_fast(self, start_address, word_count):

        # N.B., This does NOT model the behavior of splitting long bursts into subbursts of at most 256 words.

        yield self.pi.ale_l.eq(0)
        yield Delay(20e-9)
        yield self.pi.ad.i.eq((start_address >> 16) & 0xFFFF)
        yield Delay(92e-9)
        yield self.pi.ale_h.eq(1)
        yield Delay(20e-9)
        yield self.pi.ad.i.eq(start_address & 0xFFFF)
        yield Delay(92e-9)
        yield self.pi.ale_l.eq(1)
        yield Delay(1044e-9)

        address = start_address
        result = []

        for i in range(word_count):
            yield self.pi.read.eq(1)
            yield Delay(304e-9)

            word = yield self.pi.ad.o
            yield self.pi.read.eq(0)
            yield Delay(416e-9)

            result.append((address, word))
            address += 2

        yield self.pi.ale_h.eq(0)
        yield Delay(32e-9)

        return result
