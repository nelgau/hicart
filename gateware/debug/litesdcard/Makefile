DEBUG_SRC = $(wildcard rtl/debug/*.v)
DEBUG_OBJ = build/top_tb_debug.vvp
DEBUG_WAVE = traces/out_debug.vcd

GEN_SRC = $(wildcard rtl/gen/*.v)
GEN_OBJ = build/top_tb_gen.vvp
GEN_WAVE = traces/out_gen.vcd

TOP_MOD = -s top_tb -s waveform
IV_FLAGS = -g2012 -pfileline=1

all: $(DEBUG_OBJ) $(GEN_OBJ)

clean:
	rm -f build/*.vvp traces/*.vcd

run-debug: $(DEBUG_OBJ)
	vvp -n $(DEBUG_OBJ)

inspect-debug: $(DEBUG_OBJ)
	vvp ${VVP_FLAGS} $(DEBUG_OBJ)

wave-debug:
	gtkwave $(DEBUG_WAVE)

run-gen: $(GEN_OBJ)
	vvp -n $(GEN_OBJ)

inspect-gen: $(GEN_OBJ)
	vvp ${VVP_FLAGS} $(GEN_OBJ)

wave-gen:
	gtkwave $(GEN_WAVE)

$(DEBUG_OBJ): $(DEBUG_SRC)
	iverilog -o $@ $(IV_FLAGS) $(TOP_MOD) $^

$(GEN_OBJ): $(GEN_SRC)
	iverilog -o $@ $(IV_FLAGS) $(TOP_MOD) $^

.PHONY: all clean
.PHONY: run-debug inspect-debug wave-debug
.PHONY: run-gen inspect-gen wave-gen
