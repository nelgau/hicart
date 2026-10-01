#ifndef __INTERFACE_H
#define __INTERFACE_H

#include <stdint.h>

// Much of this was derived from lambdasoc-bios.

#define CSR_MSTATUS 0x300

#define MSTATUS_MIE 0x00000008

// CSR

#define read_csr(reg) ({ unsigned long __tmp; \
    asm volatile ("csrr %0, " #reg : "=r"(__tmp)); \
    __tmp; })

#define write_csr(reg, val) ({ \
    asm volatile ("csrw " #reg ", %0" :: "rK"(val)); })

#define set_csr(reg, bit) ({ unsigned long __tmp; \
    asm volatile ("csrrs %0, " #reg ", %1" : "=r"(__tmp) : "rK"(bit)); \
    __tmp; })

#define clear_csr(reg, bit) ({ unsigned long __tmp; \
    asm volatile ("csrrc %0, " #reg ", %1" : "=r"(__tmp) : "rK"(bit)); \
    __tmp; })

static inline void reset(void) {
    asm volatile ("j _reset_vector");
}

// IRQ

static inline uint32_t irq_getie(void) {
    return (read_csr(mstatus) & MSTATUS_MIE) != 0;
}

static inline void irq_setie(uint32_t ie) {
    if (ie) {
        set_csr(mstatus, MSTATUS_MIE);
    } else {
        clear_csr(mstatus, MSTATUS_MIE);
    }
}

static inline uint32_t irq_getmask(void) {
    return read_csr(0x330);
}

static inline void irq_setmask(uint32_t value) {
    write_csr(0x330, value);
}

static inline uint32_t irq_pending(void) {
    return read_csr(0x360);
}

#endif
