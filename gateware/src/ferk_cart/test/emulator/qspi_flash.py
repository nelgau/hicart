from amaranth import *
from amaranth.sim import *


class QSPIFlashEmulator:

    def __init__(self, qspi, data):
        self.qspi = qspi
        self.data = data

    def emulate(self):    
        while True:
            yield self.qspi.d.i.eq(0)

            yield from self._wait_for_cs()            

            command = yield from self._read_spi(8)
            if command is None:
                continue

            assert command == 0xEB

            address = yield from self._read_qspi(6)
            if address is None:
                continue

            mode = yield from self._read_qspi(2)
            if mode is None:
                continue

            assert mode == 0xF0  

            dummy = yield from self._read_qspi(3)
            if dummy is None:
                continue

            while True:
                data = self._load_data(address)
                bursting = yield from self._write_qspi(2, data)
                if not bursting:
                    break
                address += 1

    def _load_data(self, address):
        if address < len(self.data):
            return self.data[address]
        else:
            return 0xFF

    def _wait_for_cs(self):
        while (yield self.qspi.cs_n):
            yield

    def _read_spi(self, bit_count):
        result = 0

        for i in range(bit_count):
            aborted = yield from self._wait_for_next_clock()
            if aborted:
                return None

            bit = (yield self.qspi.d.o[0])
            result = (result << 1) | bit
            yield

        return result

    def _read_qspi(self, nibble_count):
        result = 0

        for i in range(nibble_count):
            aborted = yield from self._wait_for_next_clock()
            if aborted:
                return None

            nibble = (yield self.qspi.d.o)
            result = (result << 4) | nibble
            yield

        return result

    def _write_qspi(self, nibble_count, data):
        nibbles = []
        for i in range(nibble_count):
            nibbles.append(data & 0xF)
            data >>= 4

        for nibble in reversed(nibbles):
            aborted = yield from self._wait_for_next_clock()
            if aborted:
                return False

            yield self.qspi.d.i.eq(nibble)
            yield

        return True

    def _wait_for_next_clock(self):        
        while True:
            if (yield self.qspi.cs_n):
                return True

            if (yield self.qspi.sck):
                return False
            
            yield
