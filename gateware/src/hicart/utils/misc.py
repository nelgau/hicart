from amaranth import *


class FFDelay(Elaboratable):

    def __init__(self, i, o, *, o_domain="sync", init=None, reset_less=True, stages=2):
        self.i = i
        self.o = o

        self._init       = init
        self._reset_less = reset_less
        self._o_domain   = o_domain
        self._stages     = stages

    def elaborate(self, platform):
        m = Module()

        if self._stages > 0:
            flops = [Signal(self.i.shape(), name=f"stage{index}",
                            init=self._init, reset_less=self._reset_less)
                    for index in range(self._stages)]
            for i, o in zip((self.i, *flops), flops):
                m.d[self._o_domain] += o.eq(i)
            m.d.comb += self.o.eq(flops[-1])
        else:
            m.d.comb += self.o.eq(self.i)

        return m
