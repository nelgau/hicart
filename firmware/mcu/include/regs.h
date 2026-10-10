#ifndef __REGS_H
#define __REGS_H

#define REG_BASE            0xC0000000
#define REG_HANDSHAKE       (REG_BASE + 0x00)
#define REG_COMMAND         (REG_BASE + 0x04)
#define REG_ARG1            (REG_BASE + 0x08)
#define REG_ARG2            (REG_BASE + 0x0C)
#define REG_RESULT          (REG_BASE + 0x10)

#define HANDSHAKE_PENDING   0x1
#define HANDSHAKE_SUCCESS   0x0
#define HANDSHAKE_ERROR     0x2

static inline uint32_t reg_read(uint32_t address) {
    return *(volatile uint32_t *)address;
}

static inline void reg_write(uint32_t address, uint32_t data) {
    *((volatile uint32_t *)address) = data;
}

#endif
