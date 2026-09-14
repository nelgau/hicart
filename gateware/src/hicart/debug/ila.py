import collections
import collections.abc
import math
import operator
import os
import subprocess
import sys
import tempfile

from abc import ABCMeta, abstractmethod
from functools import reduce

from amaranth import *
from amaranth.hdl.rec import Record
from amaranth.lib import wiring
from amaranth.lib.cdc import FFSynchronizer
from amaranth.lib.fifo import AsyncFIFOBuffered
from amaranth.lib.memory import Memory
from vcd import VCDWriter
from vcd.gtkw import GTKWSave

from hicart.interface.ft245 import FT245Interface
from hicart.soc.stream import ByteDownConverter


#
# General Components
#

# Derived from Appolo FPGA (Great Scott Gadgets)

class bits:
    """An immutable bit sequence, like ``bytes`` but for bits.

    This bit sequence is ordered from LSB to MSB; this is the direction in which it is converted
    to and from iterators, and to and from bytes. Note, however, that it is converted to and from
    strings (which should be only used where a human-readable form is required) from MSB to LSB;
    this matches the way integer literals are written, as well as values in datasheets and other
    documentation.
    """
    __slots__ = ["_len_", "_int_"]

    @classmethod
    def from_int(cls, value, length=None):
        value = operator.index(value)
        if length is None:
            if value < 0:
                raise ValueError("invalid negative input for bits(): '{}'".format(value))
            length = value.bit_length()
        else:
            length = operator.index(length)
            value &= ~(-1 << length)
        inst = object.__new__(cls)
        inst._len_ = length
        inst._int_ = value
        return inst

    @classmethod
    def from_str(cls, value):
        value  = re.sub(r"[\s_]", "", value)
        if value:
            if value[0] == "-":
                raise ValueError("invalid negative input for bits(): '{}'".format(value))
            elif value[0] == "+":
                length = len(value) - 1
            else:
                length = len(value)
            return cls.from_int(int(value, 2), length)
        else:
            return cls.from_int(0)

    @classmethod
    def from_iter(cls, iterator):
        length = -1
        value  = 0
        for length, bit in enumerate(iterator):
            value |= bool(bit) << length
        return cls.from_int(value, length + 1)

    @classmethod
    def from_bytes(cls, value, length, byteorder='little'):
        return cls.from_int(int.from_bytes(value, byteorder), length)

    def __new__(cls, value=0, length=None, byteorder='little'):
        if isinstance(value, cls):
            if length is None:
                return value
            else:
                return cls.from_int(value._int_, length)
        if isinstance(value, int):
            return cls.from_int(value, length)
        if isinstance(value, str):
            if length is not None:
                raise ValueError("invalid input for bits(): when converting from str "
                                 "length must not be provided")
            return cls.from_str(value)
        if isinstance(value, (bytes, bytearray, memoryview)):
            if length is None:
                raise ValueError("invalid input for bits(): when converting from bytes "
                                 "length must be provided")
            return cls.from_bytes(value, length, byteorder)
        if isinstance(value, collections.abc.Iterable):
            if length is not None:
                raise ValueError("invalid input for bits(): when converting from an iterable "
                                 "length must not be provided")
            return cls.from_iter(value)
        raise TypeError("invalid input for bits(): cannot convert from {}"
                        .format(value.__class__.__name__))

    def __len__(self):
        return self._len_

    def __bool__(self):
        return bool(self._len_)

    def to_int(self):
        return self._int_

    __int__ = to_int

    def to_str(self):
        if self._len_:
            return format(self._int_, "0{}b".format(self._len_))
        return ""

    __str__ = to_str

    def to_bytes(self, byteorder="little"):
        return self._int_.to_bytes((self._len_ + 7) // 8, byteorder)

    __bytes__ = to_bytes

    def __repr__(self):
        return "bits('{}')".format(self)

    def __getitem__(self, key):
        if isinstance(key, int):
            if key < 0:
                return (self._int_ >> (self._len_ - key)) & 1
            else:
                return (self._int_ >> key) & 1
        if isinstance(key, slice):
            start, stop, step = key.indices(self._len_)
            assert step == 1
            if stop < start:
                return self.__class__()
            else:
                return self.__class__(self._int_ >> start, stop - start)
        raise TypeError("bits indices must be integers or slices, not {}"
                        .format(key.__class__.__name__))

    def __iter__(self):
        for bit in range(self._len_):
            yield (self._int_ >> bit) & 1

    def __eq__(self, other):
        try:
            other = self.__class__(other)
        except TypeError:
            return False
        return self._len_ == other._len_ and self._int_ == other._int_

    def __add__(self, other):
        other = self.__class__(other)
        return self.__class__(self._int_ | (other._int_ << self._len_),
                              self._len_ + other._len_)

    def __radd__(self, other):
        other = self.__class__(other)
        return other + self

    def __mul__(self, other):
        if isinstance(other, int):
            return self.__class__(reduce(lambda a, b: (a << self._len_) | b,
                                         (self._int_ for _ in range(other)), 0),
                                  self._len_ * other)
        return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __and__(self, other):
        other = self.__class__(other)
        return self.__class__(self._int_ & other._int_, max(self._len_, other._len_))

    def __rand__(self, other):
        other = self.__class__(other)
        return self & other

    def __or__(self, other):
        other = self.__class__(other)
        return self.__class__(self._int_ | other._int_, max(self._len_, other._len_))

    def __ror__(self, other):
        other = self.__class__(other)
        return self | other

    def __xor__(self, other):
        other = self.__class__(other)
        return self.__class__(self._int_ ^ other._int_, max(self._len_, other._len_))

    def __rxor__(self, other):
        other = self.__class__(other)
        return self ^ other

    def reversed(self):
        value = 0
        for bit in range(self._len_):
            value <<= 1
            if (self._int_ >> bit) & 1:
                value |= 1
        return self.__class__(value, self._len_)

# Derived from Luna (Great Scott Gadgets).

class StreamInterface(Record):
    """ Simple record implementing a unidirectional data stream.

    Attributes
    -----------
    valid: Signal(), from originator
        Indicates that the current payload bytes are valid pieces of the current transaction.
    first: Signal(), from originator
        Indicates that the payload byte is the first byte of a new packet.
    last: Signal(), from originator
        Indicates that the payload byte is the last byte of the current packet.
    payload: Signal(payload_width), from originator
        The data payload to be transmitted.

    ready: Signal(), from receiver
        Indicates that the receiver will accept the payload byte at the next active
        clock edge. Can be de-asserted to put backpressure on the transmitter.

    Parameters
    ----------
    payload_width: int
        The width of the stream's payload, in bits.
    """

    def __init__(self, payload_width=8):
        super().__init__([
            ('valid',    1),
            ('ready',    1),

            ('first',    1),
            ('last',     1),

            ('payload',  payload_width),
        ])

class IntegratedLogicAnalyzer(Elaboratable):
    """ Super-simple integrated-logic-analyzer generator class for LUNA.

    Attributes
    ----------
    trigger: Signal(), input
        A strobe that determines when we should start sampling.
    sampling: Signal(), output
        Indicates when sampling is in progress.

    complete: Signal(), output
        Indicates when sampling is complete and ready to be read.

    captured_sample_number: Signal(), input
        Selects which sample the ILA will output. Effectively the address for the ILA's
        sample buffer.
    captured_sample: Signal(), output
        The sample corresponding to the relevant sample number.
        Can be broken apart by using Cat(*signals).

    Parameters
    ----------
    signals: iterable of Signals
        An iterable of signals that should be captured by the ILA.
    sample_depth: int
        The depth of the desired buffer, in samples.

    domain: string
        The clock domain in which the ILA should operate.
    sample_rate: float
        Cosmetic indication of the sample rate. Used to format output.
    samples_pretrigger: int
        The number of our samples which should be captured _before_ the trigger.
        This also can act like an implicit synchronizer; so asynchronous inputs
        are allowed if this number is >= 2. Note that the trigger strobe is read
        on the rising edge of the clock.
    """

    def __init__(self, *, signals, sample_depth, domain="sync", sample_rate=60e6, samples_pretrigger=1):
        self.domain             = domain
        self.signals            = signals
        self.inputs             = Cat(*signals)
        self.sample_width       = len(self.inputs)
        self.sample_depth       = sample_depth
        self.samples_pretrigger = samples_pretrigger
        self.sample_rate        = sample_rate
        self.sample_period      = 1 / sample_rate

        #
        # Create a backing store for our samples.
        #
        self.mem = Memory(shape=self.sample_width, depth=sample_depth, init=[])


        #
        # I/O port
        #
        self.trigger  = Signal()
        self.sampling = Signal()
        self.complete = Signal()

        self.captured_sample_number = Signal(range(0, self.sample_depth))
        self.captured_sample        = Signal(self.sample_width)


    def elaborate(self, platform):
        m  = Module()

        # Memory ports.
        write_port = self.mem.write_port()
        read_port  = self.mem.read_port(domain="sync")
        m.submodules['ila_buffer'] = self.mem

        # If necessary, create synchronized versions of the relevant signals.
        if self.samples_pretrigger >= 2:
            delayed_inputs = Signal.like(self.inputs)
            m.submodules += FFSynchronizer(self.inputs,  delayed_inputs,
                stages=self.samples_pretrigger)
        elif self.samples_pretrigger == 1:
            delayed_inputs = Signal.like(self.inputs)
            m.d.sync += delayed_inputs.eq(self.inputs)
        else:
            delayed_inputs  = self.inputs

        # Counter that keeps track of our write position.
        write_position = Signal(range(0, self.sample_depth))

        # Set up our write port to capture the input signals,
        # and our read port to provide the output.
        m.d.comb += [
            write_port.data        .eq(delayed_inputs),
            write_port.addr        .eq(write_position),

            self.captured_sample   .eq(read_port.data),
            read_port.addr         .eq(self.captured_sample_number)
        ]

        # Don't sample unless our FSM asserts our sample signal explicitly.
        m.d.sync += write_port.en.eq(0)

        with m.FSM(name="ila_state") as fsm:

            m.d.comb += self.sampling.eq(~fsm.ongoing("IDLE"))

            # IDLE: wait for the trigger strobe
            with m.State('IDLE'):

                with m.If(self.trigger):
                    m.next = 'SAMPLE'

                    # Grab a sample as our trigger is asserted.
                    m.d.sync += [
                        write_port.en  .eq(1),
                        write_position .eq(0),

                        self.complete  .eq(0),
                    ]

            # SAMPLE: do our sampling
            with m.State('SAMPLE'):

                # Sample until we run out of samples.
                m.d.sync += [
                    write_port.en  .eq(1),
                    write_position .eq(write_position + 1),
                ]

                # If this is the last sample, we're done. Finish up.
                with m.If(write_position + 1 == self.sample_depth):
                    m.next = "IDLE"

                    m.d.sync += [
                        self.complete .eq(1),
                        write_port.en .eq(0)
                    ]


        # Convert our sync domain to the domain requested by the user, if necessary.
        if self.domain != "sync":
            m = DomainRenamer(self.domain)(m)

        return m


class StreamILA(Elaboratable):
    """ Super-simple ILA that outputs its samples over a Stream.
    Create a receiver for this object by calling apollo.ila_receiver_for(<this>).

    This protocol is simple: we wait for a trigger; and then broadcast our samples.
    We broadcast one buffer of samples per each subsequent trigger.

    Attributes
    ----------
    trigger: Signal(), input
        A strobe that determines when we should start sampling.
    sampling: Signal(), output
        Indicates when sampling is in progress.
    complete: Signal(), output
        Indicates when sampling is complete and ready to be read.

    stream: output stream
        Stream output for the ILA.

    Parameters
    ----------
    signals: iterable of Signals
        An iterable of signals that should be captured by the ILA.
    sample_depth: int
        The depth of the desired buffer, in samples.

    domain: string
        The clock domain in which the ILA should operate.
    o_domain: string
        The clock domain in which the output stream will be generated.
        If omitted, defaults to the same domain as the core ILA.
    samples_pretrigger: int
        The number of our samples which should be captured _before_ the trigger.
        This also can act like an implicit synchronizer; so asynchronous inputs
        are allowed if this number is >= 2.
    """

    def __init__(self, *, signals, sample_depth, o_domain=None, **kwargs):
        # Extract the domain from our keyword arguments, and then translate it to sync
        # before we pass it back below. We'll use a DomainRenamer at the boundary to
        # handle non-sync domains.
        self.domain = kwargs.get('domain', 'sync')
        kwargs['domain'] = 'sync'

        self._o_domain = o_domain if o_domain else self.domain

        # Create our core integrated logic analyzer.
        self.ila = IntegratedLogicAnalyzer(
            signals=signals,
            sample_depth=sample_depth,
            **kwargs)

        # Copy some core parameters from our inner ILA.
        self.signals       = signals
        self.sample_width  = self.ila.sample_width
        self.sample_depth  = self.ila.sample_depth
        self.sample_rate   = self.ila.sample_rate
        self.sample_period = self.ila.sample_period

        # Bolster our bits per sample "word" up to a power of two.
        self.bits_per_sample = 2 ** ((self.ila.sample_width - 1).bit_length())
        self.bytes_per_sample = (self.bits_per_sample + 7) // 8

        #
        # I/O port
        #
        self.stream  = StreamInterface(payload_width=self.bits_per_sample)
        self.trigger = Signal()


        # Expose our ILA's trigger and status ports directly.
        self.sampling = self.ila.sampling
        self.complete = self.ila.complete


    def elaborate(self, platform):
        m  = Module()
        m.submodules.ila = ila = self.ila

        if self._o_domain == self.domain:
            in_domain_stream = self.stream
        else:
            in_domain_stream = StreamInterface(payload_width=self.bits_per_sample)

        # Count where we are in the current transmission.
        current_sample_number = Signal(range(0, ila.sample_depth))

        # Always present the current sample number to our ILA, and the current
        # sample value to the UART.
        m.d.comb += [
            ila.captured_sample_number  .eq(current_sample_number),
            in_domain_stream.payload    .eq(ila.captured_sample)
        ]

        with m.FSM():

            # IDLE -- we're currently waiting for a trigger before capturing samples.
            with m.State("IDLE"):

                # Always allow triggering, as we're ready for the data.
                m.d.comb += self.ila.trigger.eq(self.trigger)

                # Once we're triggered, move onto the SAMPLING state.
                with m.If(self.trigger):
                    m.next = "SAMPLING"


            # SAMPLING -- the internal ILA is sampling; we're now waiting for it to
            # complete. This state is similar to IDLE; except we block triggers in order
            # to cleanly avoid a race condition.
            with m.State("SAMPLING"):

                # Once our ILA has finished sampling, prepare to read out our samples.
                with m.If(self.ila.complete):
                    m.d.sync += [
                        current_sample_number  .eq(0),
                        in_domain_stream.first      .eq(1)
                    ]
                    m.next = "SENDING"


            # SENDING -- we now have a valid buffer of samples to send up to the host;
            # we'll transmit them over our stream interface.
            with m.State("SENDING"):
                data_valid = Signal(init=1)
                m.d.comb += [
                    # While we're sending, we're always providing valid data to the UART.
                    in_domain_stream.valid  .eq(data_valid),

                    # Indicate when we're on the last sample.
                    in_domain_stream.last   .eq(current_sample_number == (self.sample_depth - 1))
                ]

                # Each time the UART accepts a valid word, move on to the next one.
                with m.If(in_domain_stream.ready):
                    with m.If(data_valid):
                        m.d.sync += [
                            current_sample_number   .eq(current_sample_number + 1),
                            data_valid              .eq(0),
                            in_domain_stream.first  .eq(0)
                        ]

                        # If this was the last sample, we're done! Move back to idle.
                        with m.If(in_domain_stream.last):
                            m.next = "IDLE"
                    with m.Else():
                        m.d.sync += data_valid.eq(1)


        # If we're not streaming out of the same domain we're capturing from,
        # we'll add some clock-domain crossing hardware.
        if self._o_domain != self.domain:
            in_domain_signals  = Cat(
                in_domain_stream.first,
                in_domain_stream.payload,
                in_domain_stream.last
            )
            out_domain_signals = Cat(
                self.stream.first,
                self.stream.payload,
                self.stream.last
            )

            # Create our async FIFO...
            m.submodules.cdc = fifo = AsyncFIFOBuffered(
                width=len(in_domain_signals),
                depth=16,
                w_domain="sync",
                r_domain=self._o_domain
            )

            m.d.comb += [
                # ... fill it from our in-domain stream...
                fifo.w_data             .eq(in_domain_signals),
                fifo.w_en               .eq(in_domain_stream.valid),
                in_domain_stream.ready  .eq(fifo.w_rdy),

                # ... and output it into our outupt stream.
                out_domain_signals      .eq(fifo.r_data),
                self.stream.valid       .eq(fifo.r_rdy),
                fifo.r_en               .eq(self.stream.ready)
            ]

        # Convert our sync domain to the domain requested by the user, if necessary.
        if self.domain != "sync":
            m = DomainRenamer(self.domain)(m)

        return m


class ILAFrontend(metaclass=ABCMeta):
    """ Class that communicates with an ILA module and emits useful output. """

    def __init__(self, ila):
        """
        Parameters:
            ila -- The ILA object to work with.
        """
        self.ila = ila
        self.samples = None


    @abstractmethod
    def _read_samples(self):
        """ Read samples from the target ILA. Should return an iterable of samples. """


    def _parse_sample(self, raw_sample):
        """ Converts a single binary sample to a dictionary of names -> sample values. """

        position = 0
        sample   = {}

        # Split our raw, bits(0) signal into smaller slices, and associate them with their names.
        for signal in self.ila.signals:
            signal_width = len(signal)
            signal_bits  = raw_sample[position : position + signal_width]
            position += signal_width

            sample[signal.name] = signal_bits

        return sample


    def _parse_samples(self, raw_samples):
        """ Converts raw, binary samples to dictionaries of name -> sample. """
        return [self._parse_sample(sample) for sample in raw_samples]


    def refresh(self):
        """ Fetches the latest set of samples from the target ILA. """
        self.samples = self._parse_samples(self._read_samples())


    def enumerate_samples(self):
        """ Returns an iterator that returns pairs of (timestamp, sample). """

        # If we don't have any samples, fetch samples from the ILA.
        if self.samples is None:
            self.refresh()

        timestamp = 0

        # Iterate over each sample...
        for sample in self.samples:
            yield timestamp, sample

            # ... and advance the timestamp by the relevant interval.
            timestamp += self.ila.sample_period


    def print_samples(self):
        """ Simple method that prints each of our samples; for simple CLI debugging."""

        for timestamp, sample in self.enumerate_samples():
            timestamp_scaled = 1000000 * timestamp
            print(f"{timestamp_scaled:08f}us: {sample}")



    def emit_vcd(self, filename, *, gtkw_filename=None, add_clock=True):
        """ Emits a VCD file containing the ILA samples.

        Parameters:
            filename      -- The filename to write to, or '-' to write to stdout.
            gtkw_filename -- If provided, a gtkwave save file will be generated that
                             automatically displays all of the relevant signals in the
                             order provided to the ILA.
            add_clock     -- If true or not provided, adds a replica of the ILA's sample
                             clock to make change points easier to see.
        """

        # Select the file-like object we're working with.
        if filename == "-":
            stream = sys.stdout
            close_after = False
        else:
            stream = open(filename, 'w')
            close_after = True

        # Create our basic VCD.
        with VCDWriter(stream, timescale=f"1 ns", date='today') as writer:
            first_timestamp = math.inf
            last_timestamp  = 0

            signals = {}

            # If we're adding a clock...
            if add_clock:
                clock_value  = 1
                clock_signal = writer.register_var('ila', 'ila_clock', 'integer', size=1, init=clock_value ^ 1)

            # Create named values for each of our signals.
            for signal in self.ila.signals:
                signals[signal.name] = writer.register_var('ila', signal.name, 'integer', size=len(signal))

            # Dump the each of our samples into the VCD.
            clock_time = 0
            for timestamp, sample in self.enumerate_samples():
                for signal_name, signal_value in sample.items():

                    # If we're adding a clock signal, add any changes necessary since
                    # the last value-change.
                    if add_clock:
                        while clock_time < timestamp:
                            writer.change(clock_signal, clock_time / 1e-9, clock_value)

                            clock_value ^= 1
                            clock_time  += (self.ila.sample_period / 2)

                    # Register the signal change.
                    writer.change(signals[signal_name], timestamp / 1e-9, signal_value.to_int())


        # If we're generating a GTKW, delegate that to our helper function.
        if gtkw_filename:
            assert(filename != '-')
            self._emit_gtkw(gtkw_filename, filename, add_clock=add_clock)


    def _emit_gtkw(self, filename, dump_filename, *, add_clock=True):
        """ Emits a GTKWave save file to accompany a generated VCD.

        Parameters:
            filename      -- The filename to write the GTKW save to.
            dump_filename -- The filename of the VCD that should be opened with this save.
            add_clock     -- True iff a clock signal should be added to the GTKW save.
        """

        with open(filename, 'w') as f:
            gtkw = GTKWSave(f)

            # Comments / context.
            gtkw.comment("Generated by the LUNA ILA.")

            # Add a reference to the dumpfile we're working with.
            gtkw.dumpfile(dump_filename)

            # If we're adding a clock, add it to the top of the view.
            gtkw.trace('ila.ila_clock')

            # Add each of our signals to the file.
            for signal in self.ila.signals:
                gtkw.trace(f"ila.{signal.name}")


    def interactive_display(self, *, add_clock=True):
        """ Attempts to spawn a GTKWave instance to display the ILA results interactively. """

        # Hack: generate files in a way that doesn't trip macOS's fancy guards.
        try:
            vcd_filename = os.path.join(tempfile.gettempdir(), os.urandom(24).hex() + '.vcd')
            gtkw_filename = os.path.join(tempfile.gettempdir(), os.urandom(24).hex() + '.gtkw')

            self.emit_vcd(vcd_filename, gtkw_filename=gtkw_filename)
            subprocess.run(["gtkwave", "-f", vcd_filename, "-a", gtkw_filename])
        finally:
            os.remove(vcd_filename)
            os.remove(gtkw_filename)

#
# Home Invader Platform
#

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
        ]

        # wiring.connect(m, iface.bus, usb_fifo)

        m.d.comb += [
            iface.bus.d.i       .eq(usb_fifo.d.i),
            iface.bus.rxf.i     .eq(usb_fifo.rxf.i),
            iface.bus.txe.i     .eq(usb_fifo.txe.i),
            iface.bus.clkout.i  .eq(usb_fifo.clkout.i),

            usb_fifo.d.o        .eq(iface.bus.d.o),
            usb_fifo.d.oe       .eq(iface.bus.d.oe),
            usb_fifo.rd.o       .eq(iface.bus.rd.o),
            usb_fifo.wr.o       .eq(iface.bus.wr.o),
            usb_fifo.siwu.o     .eq(iface.bus.siwu.o),
            usb_fifo.oe.o       .eq(iface.bus.oe.o),
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

    def interactive_display(self, *, add_clock=True):
        """ Attempts to spawn a GTKWave instance to display the ILA results interactively. """

        # Hack: generate files in a way that doesn't trip macOS's fancy guards.
        try:
            vcd_filename = os.path.join(tempfile.gettempdir(), os.urandom(24).hex() + '.vcd')
            gtkw_filename = os.path.join(tempfile.gettempdir(), os.urandom(24).hex() + '.gtkw')

            self.emit_vcd(vcd_filename, gtkw_filename=gtkw_filename)

            # subprocess.run(["gtkwave", "-f", vcd_filename, "-a", gtkw_filename])
            subprocess.run(["surfer", vcd_filename])
        finally:
            print("Warning: VCD/GTKW left on filesystem. See ILA source code.")
            # os.remove(vcd_filename)
            # os.remove(gtkw_filename)
