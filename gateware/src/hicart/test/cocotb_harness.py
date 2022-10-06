# This file was largely derived from the implementation of amaranth-cocotb.
# See https://github.com/andresdemski/nmigen-cocotb/blob/master/amaranth_cocotb/amaranth_cocotb.py

from cocotb_test.simulator import Icarus
from amaranth import Fragment
from amaranth.back import verilog
from amaranth.cli import main_parser, main_runner
import tempfile
import os
import shutil
import inspect


compile_args_waveforms = ['-s', 'cocotb_waveform_module']

verilog_waveforms = """

module cocotb_waveform_module;
   initial begin
      $dumpfile ("{}");
      $dumpvars (0, {});
      #1;
   end
endmodule
"""


def get_current_module():
    module = inspect.getsourcefile(inspect.stack()[1][0])
    return inspect.getmodulename(module)


def get_reset_signal(dut, cd):
    return getattr(dut, cd + '_rst')


def get_clock_signal(dut, cd):
    return getattr(dut, cd + '_clk')


def generate_verilog(verilog_file, design, platform, name='top',
                     ports=(), vcd_file=None):
    fragment = Fragment.get(design, platform)
    print(name, ports)
    output = verilog.convert(fragment, name=name, ports=ports)
    with open(verilog_file, 'w') as f:
        f.write('`timescale 1ns/1ps\n')
        f.write(output)
        if vcd_file:
            vcd_file = os.path.abspath(vcd_file)
            f.write(verilog_waveforms.format(vcd_file, name))


def copy_extra_files(extra_files, path):
    for f in extra_files:
        shutil.copy(f, path)


def dump_file(filename, content, d):
    file_path = d + '/' + filename
    if isinstance(content, bytes):
        content = content.decode('utf-8')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            c = f.read()
        if c != content:
            raise ValueError("File {!r} already exists"
                             .format(filename))
    else:
        with open(file_path, 'w') as f:
            f.write(content)
    return file_path


def run(design, module, platform=None, ports=(), name='top',
        verilog_sources=None, extra_files=None, vcd_file=None,
        simulator=Icarus, extra_args=None, extra_env=None):
    with tempfile.TemporaryDirectory() as d:
        verilog_file = d + '/nmigen_output.v'
        generate_verilog(verilog_file, design, platform, name, ports, vcd_file)
        sources = [verilog_file]
        if verilog_sources:
            sources.extend(verilog_sources)
        if extra_files:
            copy_extra_files(extra_files, d)
        if platform:
            for filename, content in platform.extra_files.items():
                filepath = dump_file(filename, content, d)
                if filename.endswith('.v') or filename.endswith('.sv'):
                    sources.append(filepath)
        compile_args = []
        if vcd_file:
            compile_args += compile_args_waveforms
        if extra_args:
            compile_args += extra_args
        os.environ['SIM'] = 'icarus'
        sim = simulator(toplevel=name,
                        module=module,
                        verilog_sources=sources,
                        compile_args=compile_args,
                        sim_build=d,
                        extra_env=extra_env)
        sim.run()
