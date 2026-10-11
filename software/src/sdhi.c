#include <libdragon.h>
#include <fatfs/ff.h>
#include <fatfs/diskio.h>
#include "cmd.h"
#include "regs.h"

#define SD_CARD_PRESENT         (1u << 0)
#define SD_CARD_READY           (1u << 1)

static char *sdhi_prefix = "sdhi:/";
static int sdhi_vol_id = -1;

static void sdhi_dma_rd(void *dram, uint32_t cart, uint32_t size)
{
    data_cache_hit_writeback_invalidate(dram, size);
    dma_read_raw_async(dram, cart, size);
    dma_wait();
}

static int sdhi_disk_initialize(void)
{
	if (cmd_send(CMD_SD_INIT, 0, 0, NULL)) {
		return STA_NOINIT;
	}
	return 0;
}

static int sdhi_disk_status(void) {
    uint32_t result;
	if (cmd_send(CMD_SD_STATUS, 0, 0, &result))	{
		return STA_NOINIT;
	}
	if (!(result & SD_CARD_PRESENT)) {
		return STA_NODISK | STA_NOINIT;
	}
	if (!(result & SD_CARD_READY)) {
		return STA_NOINIT;
	}
	return 0;
}

__attribute__((aligned(16))) static uint64_t sdhi_bounce[512 / 8];

static int sdhi_disk_read(uint8_t* buff, int64_t sector, int count)
{
	_Static_assert(FF_MIN_SS == 512, "this function assumes sector size == 512");
	_Static_assert(FF_MAX_SS == 512, "this function assumes sector size == 512");
	assertf((uint32_t)sector == sector, "unsupported access to SD card > 2 TiB");

	if (PhysicalAddr(buff) >= 0x00800000) {
    	return RES_PARERR;
	}

    int i;
    int n;

    while (count > 0) {
        n = count < SD_BUFFER_SECTORS ? count : SD_BUFFER_SECTORS;

		uint32_t result;
		if (cmd_send(CMD_SD_READ, sector, n, &result)) {
			return RES_ERROR;
		}

        if ((uintptr_t)buff & 7) {
            for (i = 0; i < n; i++) {
                sdhi_dma_rd(sdhi_bounce, SD_BUFFER_BASE + 512 * i, 512);
				memcpy(buff, sdhi_bounce, 512);
                buff += 512;
            }
        } else {
            sdhi_dma_rd(buff, SD_BUFFER_BASE, 512 * n);
            buff += 512 * n;
        }

		sector += n;
        count -= n;
    }

	return RES_OK;
}

static int sdhi_disk_write(const uint8_t* buff, int64_t sector, int count)
{
	return RES_WRPRT;
}

static int sdhi_disk_ioctl(uint8_t cmd, void* buff)
{
	switch (cmd)
	{
		case CTRL_SYNC: return RES_OK;
		default:        return RES_PARERR;
	}
}

static fat_disk_t fat_disk_sdhi =
{
	.disk_initialize = sdhi_disk_initialize,
	.disk_status = sdhi_disk_status,
	.disk_read = sdhi_disk_read,
	.disk_write = sdhi_disk_write,
	.disk_ioctl = sdhi_disk_ioctl,
};

bool sdhi_init(void) {
    sdhi_vol_id = fat_mount(sdhi_prefix, &fat_disk_sdhi, FAT_MOUNT_DEFERRED);
	if (sdhi_vol_id < 0) {
		return false;
    }
    return true;
}
