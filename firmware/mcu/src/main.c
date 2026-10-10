#include <stdint.h>
#include "cmd.h"
#include "sd.h"

int main(void)
{
    sd_init();
    sd_read(0, 2);
    sd_read(2, 2);

    while(1) {
        cmd_process();
        sd_process();
    }
}
