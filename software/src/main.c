#include <stdio.h>
#include <errno.h>
#include <libdragon.h>
#include "cmd.h"
#include "soak.h"
#include "regs.h"
#include "sdhi.h"

int main(void)
{
    console_init();

    debug_init_usblog();
    console_set_debug(true);

    sdhi_init();

    // run_soak();

    FILE *f = fopen("sdhi:/example.txt", "r");
    if (!f) {
        printf("open failed %s\n", strerror(errno));
    } else {
        char buf[128] = {0};
        fread(buf, 1, sizeof(buf) - 1, f);
        printf("%s\n", buf);
        fclose(f);
    }
}
