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

uint32_t read_reg(uint32_t address) {
    return *(volatile uint32_t *)address;
}

void write_reg(uint32_t address, uint32_t data) {
    volatile uint32_t *ptr = (uint32_t *)address;
    *ptr = data;
}

int main(void)
{
    while(1) {
        if (read_reg(REG_HANDSHAKE) & HANDSHAKE_PENDING) {
            uint32_t arg1 = read_reg(REG_ARG1);
            uint32_t result = arg1 + 1;

            write_reg(REG_RESULT, result);
            write_reg(REG_HANDSHAKE, HANDSHAKE_SUCCESS);
        }
    }
}

void isr(void)
{

}
