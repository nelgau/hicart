#include <stdint.h>
#include <stdbool.h>
#include "cmd.h"
#include "regs.h"

#define HANDSHAKE_SUCCESS   0x0
#define HANDSHAKE_PENDING   0x1
#define HANDSHAKE_ERROR     0x2

#define CMD_PING            0x0

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

static void cmd_success(uint32_t result) {
    reg_write(REG_MAILBOX_RESULT, result);
    reg_write(REG_MAILBOX_HANDSHAKE, HANDSHAKE_SUCCESS);
}

static void cmd_error(uint32_t error) {
    reg_write(REG_MAILBOX_RESULT, error);
    reg_write(REG_MAILBOX_HANDSHAKE, HANDSHAKE_ERROR);
}

void cmd_dispatch(cmd_t *cmd) {
    switch (cmd->id) {
        case CMD_PING:
            uint32_t result = (cmd->arg1 ^ rotl(cmd->arg2, 11)) + 1;
            cmd_success(result);
            break;
        default:
            cmd_success(0);
            break;
    }
}

void cmd_process(void) {
    cmd_t cmd;

    if (cmd_receive(&cmd)) {
        cmd_dispatch(&cmd);
    }
}
