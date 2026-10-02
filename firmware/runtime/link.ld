INCLUDE memory.ld

SECTIONS
{
    .text : {
        KEEP(*crt0.S.o(.init))
        KEEP(*(.init))
        *(.text .text.*)
        *(.rodata .rodata.* .srodata .srodata.*)
        . = ALIGN(4);
    } > ROM

    .data : {
        . = ALIGN(4);
        _data = . ;
        *(.data .data.*)
        __global_pointer$ = . + 0x800;
        *(.sdata .sdata.*)
        . = ALIGN(4);
        _edata = . ;
    } > RAM AT > ROM

    _data_load = LOADADDR(.data);

    .fill : {
        FILL(0x00);
        . = ORIGIN(ROM) + LENGTH(ROM) - 1;
        BYTE(0x00)
    } > ROM

    .bss (NOLOAD) : {
        . = ALIGN(4);
        _bss = . ;
        *(.sbss .sbss.*)
        *(.bss .bss.*)
        *(COMMON)
        . = ALIGN(4);
        _ebss = . ;
    } > RAM

    .stack (NOLOAD) : {
        . = ALIGN(4);
        . = . + STACK_SIZE;
        __stack_top = . ;
        . = ALIGN(4);
    } > RAM

    _end = . ;

    .riscv.attributes 0 : { *(.riscv.attributes) }
    /DISCARD/ : { *(.comment) *(.note.GNU-stack) }
}
