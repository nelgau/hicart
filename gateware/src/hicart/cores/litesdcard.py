from abc import ABCMeta, abstractmethod
import csv
import jinja2
import os
import re
import textwrap

from amaranth import *
from amaranth import tracer
from amaranth.back import verilog
from amaranth.build.plat import Platform
from amaranth.build.run import BuildPlan, BuildProducts
from amaranth.hdl.rec import Layout, DIR_FANIN, DIR_FANOUT
from amaranth.utils import log2_int

from amaranth_soc import wishbone
from amaranth_soc.memory import MemoryMap

from hicart.platforms.homeinvader_rev_a import HomeInvaderRevAPlatform


__all__ = [
    "sd_card_layout",
    "Config",
    "ECP5Config",
    "Core",
    "Builder",
]


sd_card_layout = Layout.cast([
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


class SDCard(Record):
    def __init__(self, **kwargs):
        super().__init__(sd_card_layout, **kwargs)


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

        # FIXME: Find a way to set the name of the generated core!

        # if name is not None and not isinstance(name, str):
        #     raise TypeError("Name must be a string, not {!r}".format(name))
        # self.name = name or tracer.get_var_name(depth=2 + src_loc_at)
        self.name = "litesdcard_core"

        # Was lambdasoc IRQLine instance
        self.irq = Signal(name=f"{self.name}_irq")

        self._ctrl_bus = None
        self._dma_bus = None
        self._pins = pins

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
        # 30 == 32 - log_int (32 / granularity)
        self._dma_bus = wishbone.Interface(addr_width=30, data_width=32, granularity=8, features={"cti", "bte", "err"})

        ctrl_map = MemoryMap(addr_width=1, data_width=8)

        # csv_name = f"{self.name}_csr.csv"
        csv_name = f"build/sdcard/csr.csv"
        csr_csv = build_products.get(csv_name, mode="t")
        for row in csv.reader(csr_csv.split("\n"), delimiter=","):
            if not row or row[0][0] == "#": continue
            res_type, res_name, addr, size, attrs = row
            if res_type == "csr_register":
                ctrl_map.add_resource(
                    object(),
                    name   = res_name,
                    addr   = int(addr, 16),
                    size   = int(size, 10) * 32 // ctrl_map.data_width,
                    extend = True,
                )

        self._ctrl_bus = wishbone.Interface(
            addr_width  = ctrl_map.addr_width
                        - log2_int(32 // ctrl_map.data_width),
            data_width  = 32,
            granularity = ctrl_map.data_width,
            features    = {"cti", "bte", "err"}
        )
        self._ctrl_bus.memory_map = ctrl_map

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

            "o_irq"             : self.irq
        }

        if self._pins is not None:
            core_kwargs.update({
                "i_sdcard_cmd_i"    : self._pins.cmd.i,
                "o_sdcard_cmd_o"    : self._pins.cmd.o,
                "o_sdcard_cmd_oe"   : self._pins.cmd.oe,
                "i_sdcard_dat_i"    : self._pins.dat.i,
                "o_sdcard_dat_o"    : self._pins.dat.o,
                "o_sdcard_dat_oe"   : self._pins.dat.oe,
                "o_sdcard_clk"      : self._pins.clk,
                "i_sdcard_cd"       : self._pins.cd,
            })

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
            python -m hicart.vendor.litesdcard_gen
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


def flatten_record(record):
    signals = []
    for field in record.fields.values():
        if isinstance(field, Record):
            signals += flatten_record(field)
        else:
            signals.append(field)
    return signals


def main():
    build_dir = "build/minerva_soc"

    platform = HomeInvaderRevAPlatform()

    pins = SDCard()
    
    litesdcard_config = ECP5Config(clk_freq=int(80e6))
    litesdcard_core = Core(litesdcard_config, pins=pins)
    litesdcard_core.build(Builder(), platform, build_dir)

    ports = []
    ports += flatten_record(litesdcard_core.ctrl_bus)
    ports += flatten_record(litesdcard_core.dma_bus)
    ports += flatten_record(pins)

    module = Module()
    module.submodules.litesdcard = litesdcard_core

    fragment = Fragment.get(module, platform)
    output = verilog.convert(fragment, name="litesdcard_core_amaranth", ports=ports, emit_src=False)

    print(output)


if __name__ == "__main__":
    main()
