#include <stdint.h>
#include "cmd.h"
#include "sd.h"

int main(void)
{
    sd_card_init();
    sd_card_read(0);
    sd_card_read(1);

    while(1) {
        cmd_process();
    }
}
