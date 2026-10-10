#include <stdio.h>
#include <libdragon.h>
#include "cmd.h"
#include "soak.h"

static inline uint32_t rotl(uint32_t x, unsigned n) {
    return (x << n) | (x >> (32 - n));
}

static inline uint32_t fastrand(void) {
    static uint32_t rng_state = 0x12345678;
    uint32_t x = rng_state;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    return rng_state = x;
}

void run_soak(void) {
    uint64_t i = 0;
    uint32_t n_error = 0;

    uint32_t error_arg1 = 0;
    uint32_t error_arg2 = 0;
    uint32_t error_result = 0;

    uint64_t iter_start = get_ticks();
    uint32_t iter_count = 0;

    while(1) {
        uint32_t arg1 = fastrand();
        uint32_t arg2 = fastrand();
        uint32_t expected = (arg1 ^ rotl(arg2, 11)) + 1;
        uint32_t result;

        cmd_send(CMD_PING, arg1, arg2, &result);

        if (result != expected) {
            if (n_error == 0) {
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

            printf("%08lx %08lx %08lx %08lx %08lx %5ld/s\n", iters, n_error, error_arg1,
                error_arg2, error_result, iter_rate);

            iter_start = get_ticks();
            iter_count = 0;
        }
    }
}
