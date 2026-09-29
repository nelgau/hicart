#include <stdio.h>

#include <libdragon.h>

int main(void)
{
    console_init();

    debug_init_usblog();
    console_set_debug(true);

    printf("Hello world!\n");

    uint32_t counter = 0;

    while(1) {
        io_write(0x1FFF0000, counter);
        counter++;

        wait_ms(500);

        uint32_t value = io_read(0x1FFF0000);
        printf("%d\n", (int)value);

        wait_ms(500);
    }
}
