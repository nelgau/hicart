from abc import ABCMeta, abstractmethod
import csv
import jinja2
import os
import re
import textwrap

from amaranth import *
from amaranth import tracer
from amaranth.build.plat import Platform
from amaranth.build.run import BuildPlan, BuildProducts
from amaranth.hdl.rec import DIR_FANIN, DIR_FANOUT
from amaranth.utils import log2_int

from amaranth_soc import wishbone
from amaranth_soc.memory import MemoryMap

from lambdasoc.periph import IRQLine

from hicart.platforms.homeinvader_rev_a import HomeInvaderRevAPlatform


__all__ = [
    "Config",
    "ECP5Config",
    "Core",
    "Builder",
]


class SDCard(Record):
    def __init__(self):
        super().__init__([
            ('cmd', [
                ('i',   1,  DIR_FANIN),
                ('o',   1,  DIR_FANOUT),
                ('oe',  1,  DIR_FANOUT),
            ]),
            ('dat', [
                ('i',   4,  DIR_FANIN),
                ('o',   4,  DIR_FANOUT),
                ('oe',  4,  DIR_FANOUT),
            ]),
            ('clk',     1,  DIR_FANOUT),
            ('cd',      1,  DIR_FANIN),
        ])


class Config(metaclass=ABCMeta):
    def __init__(self, *, clk_freq=int(100e6)):

        if not isinstance(clk_freq, int) or clk_freq <= 0:
            raise ValueError("LiteEth clock frequency must be a positive integer, not {!r}"
                             .format(clk_freq))

        self.clk_freq  = clk_freq

    @property
    @abstractmethod
    def vendor(self):
        raise NotImplementedError


class ECP5Config(Config):
    vendor = "lattice"


class Core(Elaboratable):

    def __init__(self, config, *, pins=None, name=None, src_loc_at=0):
        if not isinstance(config, Config):
            raise TypeError("Config must be an instance sdcard.Config, "
                            "not {!r}"
                            .format(config))
        self.config = config

        if name is not None and not isinstance(name, str):
            raise TypeError("Name must be a string, not {!r}".format(name))
        self.name = name or tracer.get_var_name(depth=2 + src_loc_at)

        self.irq = IRQLine(name=f"{self.name}_irq")

        self._ctrl_bus = None
        self._dma_bus = None

    @property
    def ctrl_bus(self):
        if self._ctrl_bus is None:
            raise AttributeError("Bus memory map has not been populated. "
                                 "Core.build(do_build=True) must be called before accessing "
                                 "Core.bus")
        return self._ctrl_bus

    @property
    def dma_bus(self):
        if self._dma_bus is None:
            raise AttributeError("Bus memory map has not been populated. "
                                 "Core.build(do_build=True) must be called before accessing "
                                 "Core.bus")
        return self._dma_bus

    def _populate_map(self, build_products):

        self._ctrl_bus = wishbone.Interface(
            addr_width=30,      # 32 - log_int (32 / granularity)
            data_width=32,
            granularity=8,
            features={"cti", "bte", "err"}
        )

        self._dma_bus = wishbone.Interface(
            addr_width=30,      # 32 - log_int (32 / granularity)
            data_width=32,
            granularity=8,
            features={"cti", "bte", "err"}
        )

    def build(self, builder, platform, build_dir, *, do_build=True, name_force=False):
        if not isinstance(builder, Builder):
            raise TypeError("Builder must be an instance of liteeth.Builder, not {!r}"
                            .format(builder))

        plan = builder.prepare(self, name_force=name_force)
        if not do_build:
            return plan

        products = plan.execute_local(f"{build_dir}/lambdasoc.cores.liteeth")
        self._populate_map(products)

        # core_src = f"liteeth_core/liteeth_core.v"
        core_src = f"build/sdcard/gateware/litesdcard_core.v"
        platform.add_file(core_src, products.get(core_src, mode="t"))

        return products

    def elaborate(self, platform):
        sdcard = SDCard()

        core_kwargs = {
            "i_clk"             : ClockSignal("sync"),
            "i_rst"             : ResetSignal("sync"),

            "i_wb_ctrl_adr"     : self.ctrl_bus.adr,
            "i_wb_ctrl_dat_w"   : self.ctrl_bus.dat_w,
            "o_wb_ctrl_dat_r"   : self.ctrl_bus.dat_r,
            "i_wb_ctrl_sel"     : self.ctrl_bus.sel,
            "i_wb_ctrl_cyc"     : self.ctrl_bus.cyc,
            "i_wb_ctrl_stb"     : self.ctrl_bus.stb,
            "o_wb_ctrl_ack"     : self.ctrl_bus.ack,
            "i_wb_ctrl_we"      : self.ctrl_bus.we,
            "i_wb_ctrl_cti"     : self.ctrl_bus.cti,
            "i_wb_ctrl_bte"     : self.ctrl_bus.bte,
            "o_wb_ctrl_err"     : self.ctrl_bus.err,

            "o_wb_dma_adr"      : self.dma_bus.adr,
            "o_wb_dma_dat_w"    : self.dma_bus.dat_w,
            "i_wb_dma_dat_r"    : self.dma_bus.dat_r,
            "o_wb_dma_sel"      : self.dma_bus.sel,
            "o_wb_dma_cyc"      : self.dma_bus.cyc,
            "o_wb_dma_stb"      : self.dma_bus.stb,
            "i_wb_dma_ack"      : self.dma_bus.ack,
            "o_wb_dma_we"       : self.dma_bus.we,
            "o_wb_dma_cti"      : self.dma_bus.cti,
            "o_wb_dma_bte"      : self.dma_bus.bte,
            "i_wb_dma_err"      : self.dma_bus.err,

            "o_sdcard_cmd_i"    : sdcard.cmd.i,
            "i_sdcard_cmd_o"    : sdcard.cmd.o,
            "i_sdcard_cmd_t"    : sdcard.cmd.t,
            "o_sdcard_dat_i"    : sdcard.dat.i,
            "i_sdcard_dat_o"    : sdcard.dat.o,
            "i_sdcard_dat_t"    : sdcard.dat.t,
            "o_sdcard_clk"      : sdcard.clk,
            "i_sdcard_cd"       : sdcard.cd,

            "o_irq"             : self.irq
        }

        return Instance(f"{self.name}", **core_kwargs)


class Builder:
    file_templates = {
        "build_{{top.name}}.sh": r"""
            # {{autogenerated}}
            set -e
            {{emit_commands()}}
        """,
    }
    command_templates = [
        r"""
            python -m hicart.cores.litesdcard_gen
                # --output-dir {{top.name}}
                # --gateware-dir {{top.name}}
                # --csr-csv {{top.name}}_csr.csv
        """,
    ]

    def __init__(self):
        self.namespace = set()

    def prepare(self, core, *, name_force=False):
        if not isinstance(core, Core):
            raise TypeError("LiteEth core must be an instance of liteeth.Core, not {!r}"
                            .format(core))

        if core.name in self.namespace and not name_force:
            raise ValueError(
                "LiteEth core name '{}' has already been used for a previous build. Building "
                "this instance may overwrite previous build products. Passing `name_force=True` "
                "will disable this check".format(core.name)
            )
        self.namespace.add(core.name)

        # autogenerated = f"Automatically generated by LambdaSoC {__version__}. Do not edit."
        autogenerated = "Automatically generated by hicart. Do not edit."

        def emit_commands():
            commands = []
            for index, command_tpl in enumerate(self.command_templates):
                command = render(command_tpl, origin="<command#{}>".format(index + 1))
                command = re.sub(r"\s+", " ", command)
                commands.append(command)
            return "\n".join(commands)

        def render(source, origin):
            try:
                source = textwrap.dedent(source).strip()
                compiled = jinja2.Template(source, trim_blocks=True, lstrip_blocks=True)
            except jinja2.TemplateSyntaxError as e:
                e.args = ("{} (at {}:{})".format(e.message, origin, e.lineno),)
                raise
            return compiled.render({
                "autogenerated": autogenerated,
                "emit_commands": emit_commands,
                "top": core,
            })

        plan = BuildPlan(script=f"build_{core.name}")
        for filename_tpl, content_tpl in self.file_templates.items():
            plan.add_file(render(filename_tpl, origin=filename_tpl),
                          render(content_tpl,  origin=content_tpl))
        return plan


def main():
    build_dir = "build/minerva_soc"

    platform = HomeInvaderRevAPlatform()
    
    litesdcard_config = ECP5Config(clk_freq=int(80e6))
    litesdcard_core = Core(litesdcard_config, pins=None)
    litesdcard_core.build(Builder(), platform, build_dir)

if __name__ == "__main__":
    main()
