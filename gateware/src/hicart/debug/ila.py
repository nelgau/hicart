from amaranth import *
from luna.gateware.debug.ila import StreamILA, ILAFrontend

from hicart.interface.ft245 import FT245Interface
from hicart.soc.stream import ByteDownConverter


class HomeInvaderILA(Elaboratable):

    def __init__(self, *, signals, sample_depth, **kwargs):
        # Extract the domain from our keyword arguments, and then translate it to sync
        # before we pass it back below. We'll use a DomainRenamer at the boundary to
        # handle non-sync domains.
        self.domain = kwargs.get('domain', 'sync')
        kwargs['domain'] = 'sync'

        # Create our core integrated logic analyzer.
        self.ila = StreamILA(
            signals=signals,
            sample_depth=sample_depth,
            **kwargs)

        # Copy some core parameters from our inner ILA.
        self.signals          = signals
        self.sample_width     = self.ila.sample_width
        self.sample_depth     = self.ila.sample_depth
        self.sample_rate      = self.ila.sample_rate
        self.sample_period    = self.ila.sample_period
        self.bits_per_sample  = self.ila.bits_per_sample
        self.bytes_per_sample = self.ila.bytes_per_sample

        # Expose our ILA's trigger and status ports directly.
        self.trigger  = self.ila.trigger
        self.sampling = self.ila.sampling
        self.complete = self.ila.complete


    def elaborate(self, platform):
        m  = Module()

        m.submodules.ila   = ila   = self.ila
        m.submodules.iface = iface = FT245Interface()
        m.submodules.dc    = dc    = ByteDownConverter(byte_width=self.bytes_per_sample)

        usb_fifo = platform.request('usb_fifo')

        m.d.comb += [
            dc.source.payload   .eq(ila.stream.payload),
            dc.source.valid     .eq(ila.stream.valid),
            ila.stream.ready    .eq(dc.source.ready),

            dc.sink             .connect(iface.tx),
            iface.bus           .connect(usb_fifo),
        ]

        # Convert our sync domain to the domain requested by the user, if necessary.
        if self.domain != "sync":
            m = DomainRenamer({"sync": self.domain})(m)

        return m


class HomeInvaderILAFrontend(ILAFrontend):
    """ UART-based ILA transport.
    Parameters
    ------------
    port: string
        The serial port to use to connect. This is typically a path on *nix systems.
    ila: IntegratedLogicAnalyzer
        The ILA object to work with.
    """

    def __init__(self, *args, ila, **kwargs):
        import pyftdi.serialext

        self._port = pyftdi.serialext.serial_for_url('ftdi://ftdi:2232h:FT5RTNBA/1', baudrate=3000000)
        self._port.reset_input_buffer()

        super().__init__(ila)


    def _split_samples(self, all_samples):
        """ Returns an iterator that iterates over each sample in the raw binary of samples. """
        from apollo_fpga.support.bits import bits

        sample_width_bytes = self.ila.bytes_per_sample

        # Iterate over each sample, and yield its value as a bits object.
        for i in range(0, len(all_samples), sample_width_bytes):
            raw_sample    = all_samples[i:i + sample_width_bytes]
            sample_length = len(Cat(self.ila.signals))

            yield bits.from_bytes(raw_sample, length=sample_length, byteorder='little')


    def _read_samples(self):
        """ Reads a set of ILA samples, and returns them. """

        sample_width_bytes = self.ila.bytes_per_sample
        total_to_read      = self.ila.sample_depth * sample_width_bytes

        # Fetch all of our samples from the given device.
        all_samples = self._port.read(total_to_read)
        return list(self._split_samples(all_samples))
