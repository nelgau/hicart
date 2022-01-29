#include <interface.h>

int main(void);

void isr(void)
{
    reset();
}

void boot(void)
{
    // Enable IRQ0 and machine interrupts
    irq_setmask(0x1);
    irq_setie(0x1);

    main();
}
