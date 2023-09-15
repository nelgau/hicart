from amaranth import *

from hicart.debug.ila import HomeInvaderILA, HomeInvaderILAFrontend
from hicart.utils.cli import main_runner


class Top(Elaboratable):

    def __init__(self):
        self.counter = Signal(16)
        self.hello   = Signal(8)

        self.ila = HomeInvaderILA(
            sample_depth=32,
            signals=[
                self.counter,
                self.hello
            ]
        )

    def interactive_display(self):
        frontend = HomeInvaderILAFrontend(ila=self.ila)
        frontend.interactive_display()

    def elaborate(self, platform):
        m = Module()
        m.submodules += self.ila

        # Generate our domain clocks/resets.
        m.submodules.car = platform.clock_domain_generator()

        # Clock divider / counter.
        m.d.sync += self.counter.eq(self.counter + 1)

        # Say "hello world" constantly over our ILA...
        letters = Array(ord(i) for i in "Hello, world! \r\n")

        current_letter = Signal(range(0, len(letters)))

        m.d.sync += current_letter.eq(current_letter + 1)
        m.d.comb += self.hello.eq(letters[current_letter])

        # Set our ILA to trigger each time the counter is at a random value.
        # This shows off our example a bit better than counting at zero.
        m.d.comb += self.ila.trigger.eq(self.counter == 227)

        # Return our elaborated module.
        return m


if __name__ == "__main__":
    top = main_runner(Top(), do_program=True)
    top.interactive_display()
