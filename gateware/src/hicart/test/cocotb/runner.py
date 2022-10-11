import os
import shutil
import tempfile

from amaranth import Fragment
from amaranth.back import verilog
from cocotb_test.simulator import run as cocotb_test_run


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


def generate_verilog(verilog_file, design, platform, name='top',
                     ports=(), vcd_file=None):
    fragment = Fragment.get(design, platform)
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
    file_path = os.path.join(d, filename)
    file_dir = os.path.dirname(file_path)

    if isinstance(content, bytes):
        content = content.decode('utf-8')

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            c = f.read()
        if c != content:
            raise ValueError("File {!r} already exists"
                             .format(filename))
    else:
        os.makedirs(file_dir, exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)

    return file_path


def run_test(design, module, platform=None, ports=(), name='top',
        verilog_sources=None, extra_files=None, vcd_file=None,
        extra_args=None, extra_env=None, testcase=None):

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

        # cocotb_test.simulator.run has a `testcase` argument that could be
        # used to restrict execution to a single cocotb.test instance.
        cocotb_test_run(
            simulator='icarus',
            toplevel=name,
            module=module,
            verilog_sources=sources,
            compile_args=compile_args,
            sim_build=d,
            extra_env=extra_env,
            testcase=testcase
        )
