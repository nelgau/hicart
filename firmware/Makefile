CC = riscv64-unknown-elf-gcc
LD = riscv64-unknown-elf-ld
OBJCOPY = riscv64-unknown-elf-objcopy
OBJDUMP = riscv64-unknown-elf-objdump
SIZE = riscv64-unknown-elf-size

TARGET = firmware

C_FILES := $(wildcard src/*.c)
AS_FILES := $(wildcard src/*.S)

OBJECTS := \
	$(C_FILES:.c=.o) \
	$(AS_FILES:.S=.o)

DEPENDS := $(C_FILES:.c=.d)

INCLUDES = -I./include
LDSCRIPT = firmware.ld

CFLAGS = -march=rv32i -mabi=ilp32 -Os -fno-builtin $(INCLUDES)
ASFLAGS = -march=rv32i -mabi=ilp32
LDFLAGS = -b elf32-littleriscv -nostdlib -T$(LDSCRIPT)

.PHONY: all clean disassemble symbols

all: $(TARGET).bin

clean:
	rm $(OBJECTS) $(DEPENDS) $(TARGET).elf $(TARGET).bin

disassemble: $(TARGET).elf
	$(OBJDUMP) -d $< | less

symbols: $(TARGET).elf
	$(OBJDUMP) -t $< | sort | less

-include $(DEPENDS)

%.o: %.c Makefile
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

%.o: %.S Makefile
	$(CC) $(ASFLAGS) -c $< -o $@

$(TARGET).elf: $(OBJECTS) $(LDSCRIPT)
	$(LD) -o $@ $(OBJECTS) $(LDFLAGS)

$(TARGET).bin: $(TARGET).elf
	$(OBJCOPY) $< $@ -O binary
