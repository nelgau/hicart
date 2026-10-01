# runtime.mk — shared build rules for soft-core firmware.
#
# A program's Makefile sets TARGET (optional) and includes this file:
#
#     TARGET := firmware
#     include ../runtime/runtime.mk
#
# Expected program layout:
#     src/        .c and .S sources
#     include/    program headers (optional)
#     memory.ld   MEMORY block, pulled in by link.ld via INCLUDE
#
# All outputs go under build/. Run make from the program's directory.

# Directory containing this file, without a trailing slash.
RUNTIME := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

PREFIX  ?= riscv64-unknown-elf-
CC      := $(PREFIX)gcc
LD      := $(PREFIX)ld
OBJCOPY := $(PREFIX)objcopy
OBJDUMP := $(PREFIX)objdump
SIZE    := $(PREFIX)size

TARGET ?= firmware
BUILD  ?= build

ARCH    := -march=rv32i_zicsr -mabi=ilp32
CFLAGS  += $(ARCH) -Os -fno-builtin -I include -I $(RUNTIME)
ASFLAGS += $(ARCH) -I $(RUNTIME)
# -L . lets link.ld's "INCLUDE memory.ld" find this program's memory.ld.
# --no-warn-rwx-segments needs binutils 2.39 or newer; drop it if ld rejects it.
LDFLAGS += -b elf32-littleriscv -nostdlib -L . -T $(RUNTIME)/link.ld --no-warn-rwx-segments

SRCS := $(wildcard src/*.c) $(wildcard src/*.S)
OBJS := $(patsubst src/%,$(BUILD)/%.o,$(SRCS)) $(BUILD)/runtime/crt0.S.o
DEPS := $(OBJS:.o=.d)

ELF := $(BUILD)/$(TARGET).elf
BIN := $(BUILD)/$(TARGET).bin

# Rebuild everything if the build rules themselves change.
RULES := Makefile $(RUNTIME)/runtime.mk

.PHONY: all clean disassemble symbols size

all: $(BIN)

# Program sources: src/foo.c -> build/foo.c.o
$(BUILD)/%.c.o: src/%.c $(RULES)
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

$(BUILD)/%.S.o: src/%.S $(RULES)
	@mkdir -p $(dir $@)
	$(CC) $(ASFLAGS) -MMD -MP -c $< -o $@

# Shared runtime sources: ../runtime/crt0.S -> build/runtime/crt0.S.o
$(BUILD)/runtime/%.S.o: $(RUNTIME)/%.S $(RULES)
	@mkdir -p $(dir $@)
	$(CC) $(ASFLAGS) -MMD -MP -c $< -o $@

$(ELF): $(OBJS) $(RUNTIME)/link.ld memory.ld
	$(LD) $(LDFLAGS) -o $@ $(OBJS)
	$(SIZE) $@

$(BIN): $(ELF)
	$(OBJCOPY) -O binary $< $@

clean:
	rm -rf $(BUILD)

disassemble: $(ELF)
	$(OBJDUMP) -d $< | less

symbols: $(ELF)
	$(OBJDUMP) -t $< | sort | less

size: $(ELF)
	$(SIZE) $<

-include $(DEPS)
