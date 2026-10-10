#include "regs.h"
#include "sd.h"

#define SPEED_INIT              (0)
#define SPEED_DEFAULT           (1)

#define OP_CMD                  (0)
#define OP_INIT                 (1)

#define DATA_DIR_NONE           (0)
#define DATA_DIR_READ           (1)
#define DATA_DIR_WRITE          (2)

#define RESP_PRESENT            (1u << 6)
#define RESP_LONG               (1u << 7)
#define RESP_WAIT_BUSY          (1u << 8)
#define RESP_CHECK_INDEX        (1u << 9)
#define RESP_CHECK_CRC          (1u << 10)

#define STATUS_BUSY             (1u << 0)
#define STATUS_DONE             (1u << 1)
#define STATUS_CARD_PRESENT     (1u << 2)

#define R_NONE                  (0)
#define R1                      (RESP_PRESENT | RESP_CHECK_INDEX | RESP_CHECK_CRC)
#define R1B                     (R1 | RESP_WAIT_BUSY)
#define R2                      (RESP_PRESENT | RESP_LONG | RESP_CHECK_CRC)
#define R3                      (RESP_PRESENT)
#define R6                      R1
#define R7                      R1

#define CMD(idx, resp)          ((idx) | (resp))

#define NO_DATA                 (DATA_DIR_NONE)
#define DATA_READ(cnt, len)     (DATA_DIR_READ | (cnt << 2) | (len << 18))


uint32_t sd_config(uint32_t speed) {
    reg_write(REG_SD_CONFIG, speed);
}

uint32_t sd_go(uint32_t op) {
    reg_write(REG_SD_GO, op);
    while (!(reg_read(REG_SD_STATUS) & STATUS_DONE)) {}
    return (reg_read(REG_SD_STATUS) >> 8) & 0xFF;
}

uint32_t sd_op_init(void) {
    return sd_go(OP_INIT);
}

uint32_t sd_op_cmd(uint32_t cmd, uint32_t arg, uint32_t data, uint32_t *resp) {
    reg_write(REG_SD_CMD, cmd);
    reg_write(REG_SD_ARG, arg);
    reg_write(REG_SD_DATA, data);
    uint32_t err = sd_go(OP_CMD);

    if (cmd & RESP_PRESENT) {
        resp[0] = reg_read(REG_SD_RESP0);
        if (cmd & RESP_LONG) {
            resp[1] = reg_read(REG_SD_RESP1);
            resp[2] = reg_read(REG_SD_RESP2);
            resp[3] = reg_read(REG_SD_RESP3);
        }
    }

    return err;
}

void sd_writer_prepare(uint32_t address) {
    reg_write(REG_SD_WRITER_ADDRESS, address);
}

uint32_t sd_card_acmd(uint16_t rca, uint32_t cmd, uint32_t arg, uint32_t *resp) {
    uint32_t r55[4];
    uint32_t err = sd_op_cmd(CMD(55, R1), rca << 16, NO_DATA, r55);
    if (err) { return err; }
    // If APP_CMD isn't set, card won't treat next command as app command.
    if (!(r55[0] & (1u << 5))) { return SD_ERR_NOT_APP_CMD; }
    return sd_op_cmd(cmd, arg, NO_DATA, resp);
}

uint32_t sd_card_init(void) {
    uint32_t resp[4], err;
    uint16_t rca;

    sd_config(SPEED_INIT);
    sd_op_init();

    err = sd_op_cmd(CMD(0, R_NONE), 0, NO_DATA, resp);
    if (err) { return err; }

    err = sd_op_cmd(CMD(8, R7), 0x1AA, NO_DATA, resp);
    if (err) { return err; }

    do {
        err = sd_card_acmd(0, CMD(41, R3), 0x40ff8000, resp);
        if (err) { return err; }
    } while(!(resp[0] & 0x80000000));

    err = sd_op_cmd(CMD(2, R2), 0, NO_DATA, resp);
    if (err) { return err; }

    err = sd_op_cmd(CMD(3, R6), 0, NO_DATA, resp);
    if (err) { return err; }
    rca = resp[0] >> 16;

    err = sd_op_cmd(CMD(7, R1B), rca << 16, NO_DATA, resp);
    if (err) { return err; }

    err = sd_card_acmd(rca, CMD(6, R1), 2, resp);
    if (err) { return err; }

    sd_config(SPEED_DEFAULT);

    return 0;
}

uint32_t sd_card_read(uint32_t sector) {
    uint32_t resp[4];
    sd_writer_prepare(0);
    return sd_op_cmd(CMD(17, R1), sector, DATA_READ(1, 512), resp);
}
