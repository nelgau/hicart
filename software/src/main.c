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

static inline uint32_t fastrand(void) {
    static uint32_t rng_state = 0x12345678;
    uint32_t x = rng_state;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    return rng_state = x;
}

static inline uint32_t rotl(uint32_t x, unsigned n) {
    return (x << n) | (x >> (32 - n));
}

static inline uint32_t run_command(uint32_t cmd, uint32_t arg1, uint32_t arg2) {
    io_write(REG_ARG1, arg1);
    io_write(REG_ARG2, arg2);
    io_write(REG_COMMAND, cmd);
    while(io_read(REG_HANDSHAKE) & HANDSHAKE_BUSY) {}
    return io_read(REG_RESULT);
}

int main(void)
{
    console_init();

    debug_init_usblog();
    console_set_debug(true);

    uint64_t i = 0;
    uint32_t n_error = 0;

    uint32_t error_cmd = 0;
    uint32_t error_arg1 = 0;
    uint32_t error_arg2 = 0;
    uint32_t error_result = 0;

    uint64_t iter_start = get_ticks();
    uint32_t iter_count = 0;

    while(1) {
        uint32_t cmd = fastrand();
        uint32_t arg1 = fastrand();
        uint32_t arg2 = fastrand();

        uint32_t expected = (arg1 ^ rotl(arg2, 11)) + cmd + 1;
        uint32_t result = run_command(cmd, arg1, arg2);

        if (result != expected) {
            if (n_error == 0) {
                error_cmd = cmd;
                error_arg1 = arg1;
                error_arg2 = arg2;
                error_result = result;
            }
            n_error++;
        }

        i++;
        iter_count++;

        if ((i & 0xFFFF) == 0) {
            uint64_t iter_ticks = get_ticks() - iter_start;
            uint32_t iter_rate = (uint32_t)((uint64_t)iter_count * TICKS_PER_SECOND / iter_ticks);
            uint32_t iters = (uint32_t)(i >> 16);

            printf("%08lx %08lx %08lx %08lx %08lx %08lx %5ld/s\n", iters, n_error, error_cmd,
                error_arg1, error_arg2, error_result, iter_rate);

            iter_start = get_ticks();
            iter_count = 0;
        }
    }
}
