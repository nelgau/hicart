from dataclasses import dataclass
from cocotb.triggers import Timer


@dataclass
class PIBus:
    ad_i: object
    ad_o: object
    ad_oe: object
    ale_l: object
    ale_h: object
    read: object
    write: object
    reset: object

    @classmethod
    def from_dut(cls, dut):
        return cls(
            ad_i=dut.ad__i,
            ad_o=dut.ad__o,
            ad_oe=dut.ad__oe,
            ale_l=dut.ale_l,
            ale_h=dut.ale_h,
            read=dut.read,
            write=dut.write,
            reset=dut.reset
        )

class PIInitiator:
    def __init__(self, bus):
        self.bus = bus

    async def begin(self):
        self.bus.ad_i.setimmediatevalue(0)
        self.bus.ale_l.setimmediatevalue(1)
        self.bus.ale_h.setimmediatevalue(0)
        self.bus.read.setimmediatevalue(0)
        self.bus.write.setimmediatevalue(0)

        await Timer(1000, units='ps')

    async def read_burst_slow(self, start_address, word_count):
        self.bus.ale_l.value = 0
        await Timer(56, units='ps')
        self.bus.ad_i.value = (start_address >> 16) & 0xFFFF
        await Timer(56, units='ps')
        self.bus.ale_h.value = 1
        await Timer(56, units='ps')
        self.bus.ad_i.value = start_address & 0xFFFF
        await Timer(56, units='ps')
        self.bus.ale_l.value = 1

        await Timer(1040, units='ps')

        # FIXME: Is this accurate? When does N64 stop driving this?
        self.bus.ad_i.value = 0

        result = []

        for i in range(word_count):
            self.bus.read.value = 1
            await Timer(304, units='ps')

            word = self.bus.ad_o.value
            self.bus.read.value = 0
            await Timer(64, units='ps')

            result.append(word)

        self.bus.ale_h.value = 1
        await Timer(2256, units='ps')

        return result

    async def read_burst_fast(self, start_address, word_count):
        self.bus.ale_l.value = 0
        await Timer(20, units='ps')
        self.bus.ad_i.value = (start_address >> 16) & 0xFFFF
        await Timer(92, units='ps')
        self.bus.ale_h.value = 1
        await Timer(20, units='ps')
        self.bus.ad_i.value = start_address & 0xFFFF
        await Timer(92, units='ps')
        self.bus.ale_l.value = 1

        await Timer(1044, units='ps')

        # FIXME: Is this accurate? When does N64 stop driving this?
        self.bus.ad_i.value = 0

        result = []

        for i in range(word_count):
            self.bus.read.value = 1
            await Timer(304, units='ps')

            word = self.bus.ad_o.value
            self.bus.read.value = 0
            await Timer(416, units='ps')

            result.append(word)

        self.bus.ale_h.value = 1
        await Timer(32, units='ps')

        return result
