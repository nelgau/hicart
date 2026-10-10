#include <libdragon.h>
#include "cmd.h"
#include "regs.h"

#define HANDSHAKE_BUSY          0x1
#define HANDSHAKE_ERROR         0x2

bool cmd_send(uint32_t id, uint32_t arg1, uint32_t arg2, uint32_t *result) {
    io_write(REG_ARG1, arg1);
    io_write(REG_ARG2, arg2);
    // Starts operation
    io_write(REG_COMMAND, id);

    uint32_t handshake;
    do {
        handshake = io_read(REG_HANDSHAKE);
    } while (handshake & HANDSHAKE_BUSY);

    *result = io_read(REG_RESULT);
    return (handshake & HANDSHAKE_ERROR);
}
