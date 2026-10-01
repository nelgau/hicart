INCLUDE memory.ld

SECTIONS
{
    .text : {
        KEEP(*(.init));
        *(.text);
        *(.rodata);
        . = ALIGN(4);
    } > ROM

    .data : {
        . = ALIGN(4);
        _data = . ;
        *(.data);
        . = ALIGN(4);
        _edata = . ;
    } > RAM AT > ROM

    .fill : {
        FILL(0x00);
        . = ORIGIN(ROM) + LENGTH(ROM) - 1;
        BYTE(0x00)
    } > ROM

    .bss (NOLOAD) : {
        . = ALIGN(4);
        _bss = . ;
        *(.bss);
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
}
