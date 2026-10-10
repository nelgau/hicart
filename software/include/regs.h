#ifndef __REGS_H
#define __REGS_H

#define REG_BASE            0x1FF00000
#define REG_HANDSHAKE       (REG_BASE + 0x00)
#define REG_COMMAND         (REG_BASE + 0x04)
#define REG_ARG1            (REG_BASE + 0x08)
#define REG_ARG2            (REG_BASE + 0x0C)
#define REG_RESULT          (REG_BASE + 0x10)

#define SD_BUFFER_BASE      0x1FFF0000
#define SD_BUFFER_SECTORS   2

#endif
