#include <stdint.h>
#include "cmd.h"
#include "sd.h"

int main(void)
{
    while(1) {
        cmd_process();
        sd_process();
    }
}
