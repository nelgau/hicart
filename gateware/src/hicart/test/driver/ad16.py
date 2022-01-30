from amaranth.sim import *

# N.B. The control signals (e.g., ale_l, ale_h, read, write) need to be inverted!

class PIInitiator:

    def __init__(self, ad16):
        self.ad16 = ad16

    def begin(self):
        yield self.ad16.ale_l.eq(1)
        yield self.ad16.ale_h.eq(0)
        yield Delay(1e-6)

    def read_burst_slow(self, start_address, word_count):
        yield self.ad16.ale_l.eq(0)
        yield Delay(56e-9)
        yield self.ad16.ad.i.eq((start_address >> 16) & 0xFFFF)
        yield Delay(56e-9)
        yield self.ad16.ale_h.eq(1)
        yield Delay(56e-9)
        yield self.ad16.ad.i.eq(start_address & 0xFFFF)
        yield Delay(56e-9)
        yield self.ad16.ale_l.eq(1)
        yield Delay(1040e-9)

        result = []

        for i in range(word_count):
            yield self.ad16.read.eq(1)
            yield Delay(304e-9)

            word = yield self.ad16.ad.o
            yield self.ad16.read.eq(0)
            yield Delay(64e-9)

            result.append(word)

        yield self.ad16.ale_h.eq(0)
        yield Delay(2256e-9)

        return result

    def read_burst_fast(self, start_address, word_count):

        # N.B., This does NOT model the behavior of splitting long bursts into subbursts of at most 256 words.

        yield self.ad16.ale_l.eq(0)
        yield Delay(20e-9)
        yield self.ad16.ad.i.eq((start_address >> 16) & 0xFFFF)
        yield Delay(92e-9)
        yield self.ad16.ale_h.eq(1)
        yield Delay(20e-9)
        yield self.ad16.ad.i.eq(start_address & 0xFFFF)
        yield Delay(92e-9)
        yield self.ad16.ale_l.eq(1)
        yield Delay(1044e-9)

        result = []

        for i in range(word_count):
            yield self.ad16.read.eq(1)
            yield Delay(304e-9)

            word = yield self.ad16.ad.o
            yield self.ad16.read.eq(0)
            yield Delay(416e-9)

            result.append(word)

        yield self.ad16.ale_h.eq(0)
        yield Delay(32e-9)

        return result

