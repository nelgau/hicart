#ifndef __SD_H
#define __SD_H

#include <stdint.h>

#define SD_CARD_PRESENT         (1u << 0)
#define SD_CARD_READY           (1u << 1)

#define SD_ERR_CMD_TIMEOUT      (1u << 8)
#define SD_ERR_CMD_FRAME        (1u << 9)
#define SD_ERR_CMD_INDEX        (1u << 10)
#define SD_ERR_CMD_CRC          (1u << 11)
#define SD_ERR_DATA_TIMEOUT     (1u << 12)
#define SD_ERR_DATA_FRAME       (1u << 13)
#define SD_ERR_DATA_CRC         (1u << 14)
#define SD_ERR_BUSY_TIMEOUT     (1u << 15)
#define SD_ERR_NOT_APP_CMD      (1u << 16)
#define SD_ERR_NO_CARD          (1u << 17)
#define SD_ERR_NOT_READY        (1u << 18)

uint32_t sd_status(void);
uint32_t sd_init(void);
uint32_t sd_read(uint32_t sector, uint32_t count);
void sd_process(void);

#endif
