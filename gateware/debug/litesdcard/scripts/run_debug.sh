#!/bin/bash
set -euxo pipefail

SRC=(
	rtl/debug/top_tb.v
	rtl/debug/top_simple.v
	rtl/debug/litesdcard_debug.v
)

TOP=(
	-s top_tb
	-s waveform
)

VVP=build/top_tb_debug.vvp

mkdir build
mkdir traces

iverilog -o $VVP -g2012 -pfileline=1 ${TOP[@]} ${SRC[@]}
vvp $VVP
