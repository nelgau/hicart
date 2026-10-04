#include <stdio.h>
#include <libdragon.h>
#include "soak.h"

int main(void)
{
    console_init();

    debug_init_usblog();
    console_set_debug(true);

    run_soak();
}
