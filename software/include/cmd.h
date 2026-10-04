#ifndef __CMD_H
#define __CMD_H

#include <stdint.h>

#define CMD_PING    0

uint32_t cmd_send(uint32_t id, uint32_t arg1, uint32_t arg2);

#endif
