#include <stdio.h>
#include <libdragon.h>
#include "soak.h"

#include "regs.h"

int main(void)
{
    console_init();

    debug_init_usblog();
    console_set_debug(true);

    run_soak();

    // char buf[512];

    // for (int i = 0; i < 512; i += 4) {
    //     *(uint32_t *)(buf + i) = io_read(SD_BUFFER_BASE + i);
    // }

    // int off = 0;
    // int width = 12;

    // for (int i = 0; i < 24; i++) {
    //     for (int j = 0; j < width; j++) {
    //         printf("%02x ", buf[off + j]);
    //     }
    //     for (int j = 0; j < width; j++) {
    //         char x = buf[off + j];
    //         if (x >= 0x20) {
    //             printf("%c", x);
    //         } else {
    //             printf(".");
    //         }
    //     }
    //     printf("\n");
    //     off += width;
    // }
}
