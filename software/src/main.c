#include <stdio.h>

#include <libdragon.h>

int main(void)
{
    console_init();

    debug_init_usblog();
    console_set_debug(true);

    dfs_init(DFS_DEFAULT_LOCATION);

    FILE *fp = fopen("rom:/data.txt", "r");
	if (fp) {
	    fseek(fp, 0, SEEK_END);
	    int size = ftell(fp);
	    rewind(fp);

	    printf("Size: %d\n", size);
    } else {
	    printf("Error opening file\n");
    }

    while(1) {}
}
