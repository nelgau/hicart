#include <libdragon.h>
#include "cmd.h"
#include "regs.h"

uint32_t cmd_send(uint32_t id, uint32_t arg1, uint32_t arg2) {
    io_write(REG_ARG1, arg1);
    io_write(REG_ARG2, arg2);
    io_write(REG_COMMAND, id);
    while(io_read(REG_HANDSHAKE) & HANDSHAKE_BUSY) {}
    return io_read(REG_RESULT);

}
