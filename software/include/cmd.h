#ifndef __CMD_H
#define __CMD_H

#include <stdint.h>

#define CMD_PING            (0x0)
#define CMD_SD_STATUS       (0x1)
#define CMD_SD_INIT         (0x2)
#define CMD_SD_READ         (0x3)

bool cmd_send(uint32_t id, uint32_t arg1, uint32_t arg2, uint32_t *result);

#endif
