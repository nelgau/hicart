#include <stdio.h>

#include <libdragon.h>

#define REG_BASE            0x1FF00000
#define REG_HANDSHAKE       (REG_BASE + 0x00)
#define REG_COMMAND         (REG_BASE + 0x04)
#define REG_ARG1            (REG_BASE + 0x08)
#define REG_ARG2            (REG_BASE + 0x0C)
#define REG_RESULT          (REG_BASE + 0x10)

#define HANDSHAKE_BUSY      0x1
#define HANDSHAKE_ERROR     0x2

void print_regs(void) {
    uint32_t handshake  = io_read(REG_HANDSHAKE);
    uint32_t command    = io_read(REG_COMMAND);
    uint32_t arg1       = io_read(REG_ARG1);
    uint32_t arg2       = io_read(REG_ARG2);
    uint32_t result     = io_read(REG_RESULT);

    printf("REGS: %08lx %08lx %08lx %08lx %08lx\n", handshake, command, arg1, arg2, result);
}

int main(void)
{
    console_init();

    debug_init_usblog();
    console_set_debug(true);

    printf("Hello world!\n");

    uint32_t counter = 0;

    while(1) {
        io_write(REG_ARG1, counter);
        io_write(REG_COMMAND, 0xFFFFEEEE);

        // print_regs();

        while(io_read(REG_HANDSHAKE) & HANDSHAKE_BUSY) {}

        // print_regs();

        uint32_t value = io_read(REG_RESULT);
        printf("%10ld %10ld %10ld\n", counter, value, value - counter);

        wait_ms(500);
        counter += 4;
    }
}
