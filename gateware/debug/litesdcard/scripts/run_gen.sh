#!/bin/bash
set -euxo pipefail

SRC=(
	rtl/gen/top_tb.v
	rtl/gen/nmigen_output.v
	rtl/gen/litesdcard_core.v
)

TOP=(
	-s top_tb
	-s waveform
)

VVP=build/top_tb_gen.vvp

mkdir -p build
mkdir -p traces

iverilog -o $VVP -g2012 -pfileline=1 ${TOP[@]} ${SRC[@]}
vvp $VVP
