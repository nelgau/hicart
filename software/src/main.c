#include <stdio.h>

#include <libdragon.h>

int main(void)
{
    console_init();

    debug_init_usblog();
    console_set_debug(true);

    printf("Hello world!\n");

    while(1) {
        uint64_t until_ms = get_ticks_ms() + 1000;
        while (get_ticks_ms() < until_ms) {}

        printf(".\n");

        io_write(0x1FFF0000, 0xFFFF0000);
    }
}
