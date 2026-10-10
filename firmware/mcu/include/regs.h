#ifndef __REGS_H
#define __REGS_H

#include <stdint.h>

#define REG_MAILBOX_BASE            0xC0000000
#define REG_MAILBOX_HANDSHAKE       (REG_MAILBOX_BASE + 0x00)
#define REG_MAILBOX_COMMAND         (REG_MAILBOX_BASE + 0x04)
#define REG_MAILBOX_ARG1            (REG_MAILBOX_BASE + 0x08)
#define REG_MAILBOX_ARG2            (REG_MAILBOX_BASE + 0x0C)
#define REG_MAILBOX_RESULT          (REG_MAILBOX_BASE + 0x10)

#define REG_SD_BASE                 0xC0000100
#define REG_SD_CONFIG               (REG_SD_BASE + 0x00)
#define REG_SD_CMD                  (REG_SD_BASE + 0x04)
#define REG_SD_ARG                  (REG_SD_BASE + 0x08)
#define REG_SD_DATA                 (REG_SD_BASE + 0x0C)
#define REG_SD_GO                   (REG_SD_BASE + 0x10)
#define REG_SD_STATUS               (REG_SD_BASE + 0x14)
#define REG_SD_RESP0                (REG_SD_BASE + 0x18)
#define REG_SD_RESP1                (REG_SD_BASE + 0x1C)
#define REG_SD_RESP2                (REG_SD_BASE + 0x20)
#define REG_SD_RESP3                (REG_SD_BASE + 0x24)

#define REG_SD_WRITER_BASE          0xC0000200
#define REG_SD_WRITER_ADDRESS       (REG_SD_WRITER_BASE + 0x00)

static inline uint32_t reg_read(uint32_t address) {
    return *(volatile uint32_t *)address;
}

static inline void reg_write(uint32_t address, uint32_t data) {
    *((volatile uint32_t *)address) = data;
}

#endif
