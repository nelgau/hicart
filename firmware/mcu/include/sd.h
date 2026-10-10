#ifndef __SD_H
#define __SD_H

#include <stdint.h>

#define SD_ERR_CMD_TIMEOUT      (1u << 0)
#define SD_ERR_CMD_FRAME        (1u << 1)
#define SD_ERR_CMD_INDEX        (1u << 2)
#define SD_ERR_CMD_CRC          (1u << 3)
#define SD_ERR_DATA_TIMEOUT     (1u << 4)
#define SD_ERR_DATA_FRAME       (1u << 5)
#define SD_ERR_DATA_CRC         (1u << 6)
#define SD_ERR_BUSY_TIMEOUT     (1u << 7)
#define SD_ERR_NOT_APP_CMD      (1u << 8)

uint32_t sd_card_init(void);
uint32_t sd_card_read(uint32_t sector);

#endif
