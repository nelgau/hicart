import time

from amaranth import *

from ferk_cart.debug.wishbone import FT245WishboneCommander, FT245WishboneRemote
from ferk_cart.utils.cli import main_runner


class Top(Elaboratable):

    def elaborate(self, platform):
        m = Module()

        leds = platform.get_leds()

        m.submodules.car         = platform.clock_domain_generator()
        m.submodules.comm = comm = FT245WishboneCommander()

        m.d.sync += comm.bus.ack.eq(0)
        with m.If(comm.bus.stb):
            m.d.sync += comm.bus.ack.eq(1)

            with m.If(comm.bus.we):
                m.d.sync += leds.eq(comm.bus.dat_w[0:8])

        m.d.comb += [
            comm.bus.dat_r.eq(comm.bus.adr + 0x45)
        ]

        return m

def run_remote():
    remote = FT245WishboneRemote()

    time.sleep(1)

    # while True:
    #     result = remote.read(0x11)
    #     print(f'{result:08X}')
    #     time.sleep(0.25)

    #     result = remote.read(0x22)
    #     print(f'{result:08X}')
    #     time.sleep(0.25)

    #     remote.write(0x11, 0x00000099)
    #     time.sleep(0.25)

    #     remote.write(0x22, 0x00000066)
    #     time.sleep(0.25)        

    count = 10000
    start_time = time.time()

    for i in range(count):
        #remote.write(0x22, 0x00000066)
        remote.read(0x22)

    end_time = time.time()
    total_time = end_time - start_time
    rate = count / total_time

    print(f"{total_time:.2f} seconds ({rate:.2f} ops/sec)")

if __name__ == "__main__":
    main_runner(Top())
    run_remote()
