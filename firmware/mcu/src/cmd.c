#include <stdint.h>
#include <stdbool.h>
#include "cmd.h"
#include "regs.h"
#include "sd.h"

#define HANDSHAKE_SUCCESS   0x0
#define HANDSHAKE_PENDING   0x1
#define HANDSHAKE_ERROR     0x2

#define CMD_PING            0x0
#define CMD_SD_STATUS       0x1
#define CMD_SD_INIT         0x2
#define CMD_SD_READ         0x3

static inline uint32_t rotl(uint32_t x, unsigned n) {
    return (x << n) | (x >> (32 - n));
}

typedef struct {
    uint32_t id;
    uint32_t arg1;
    uint32_t arg2;
} cmd_t;

static bool cmd_receive(cmd_t *cmd) {
    if (reg_read(REG_MAILBOX_HANDSHAKE) & HANDSHAKE_PENDING) {
        cmd->id = reg_read(REG_MAILBOX_COMMAND);
        cmd->arg1 = reg_read(REG_MAILBOX_ARG1);
        cmd->arg2 = reg_read(REG_MAILBOX_ARG2);
        return true;
    } else {
        return false;
    }
}

static void cmd_respond(uint32_t result, bool error) {
    reg_write(REG_MAILBOX_RESULT, result);
    reg_write(REG_MAILBOX_HANDSHAKE, error ? HANDSHAKE_ERROR : HANDSHAKE_SUCCESS);
}

void cmd_process(void) {
    cmd_t cmd;
    if (!cmd_receive(&cmd)) {
        return;
    }

    uint32_t result = 0;
    bool error = false;

    switch (cmd.id) {
        case CMD_PING:
            result = (cmd.arg1 ^ rotl(cmd.arg2, 11)) + 1;
            break;
        case CMD_SD_STATUS:
            result = sd_status();
            break;
        case CMD_SD_INIT:
            result = sd_init();
            error = (result != 0);
            break;
        case CMD_SD_READ:
            result = sd_read(cmd.arg1, cmd.arg2);
            error = (result != 0);
            break;
    }

    cmd_respond(result, error);
}
