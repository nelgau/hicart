#include <stdint.h>

#define REG_BASE            0x00006000
#define REG_HANDSHAKE       (REG_BASE + 0x00)
#define REG_COMMAND         (REG_BASE + 0x04)
#define REG_ARG1            (REG_BASE + 0x08)
#define REG_ARG2            (REG_BASE + 0x0C)
#define REG_RESULT          (REG_BASE + 0x10)

#define HANDSHAKE_PENDING   0x1
#define HANDSHAKE_SUCCESS   0x0
#define HANDSHAKE_ERROR     0x2

static inline uint32_t read_reg(uint32_t address) {
    return *(volatile uint32_t *)address;
}

static inline void write_reg(uint32_t address, uint32_t data) {
    volatile uint32_t *ptr = (uint32_t *)address;
    *ptr = data;
}

static inline uint32_t rotl(uint32_t x, unsigned n) {
    return (x << n) | (x >> (32 - n));
}

int main(void)
{
    while(1) {
        if (read_reg(REG_HANDSHAKE) & HANDSHAKE_PENDING) {
            uint32_t cmd = read_reg(REG_COMMAND);
            uint32_t arg1 = read_reg(REG_ARG1);
            uint32_t arg2 = read_reg(REG_ARG2);

            uint32_t result = (arg1 ^ rotl(arg2, 11)) + cmd + 1;

            write_reg(REG_RESULT, result);
            write_reg(REG_HANDSHAKE, HANDSHAKE_SUCCESS);
        }
    }
}
