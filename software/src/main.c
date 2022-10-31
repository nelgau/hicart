#include <libdragon.h>

#define NUM_DISPLAY 4

int main(void)
{
    controller_init();
    debug_init_isviewer();
    debug_init_usblog();

    display_init(RESOLUTION_320x240, DEPTH_32_BPP, NUM_DISPLAY, GAMMA_NONE, ANTIALIAS_OFF);
    dfs_init(DFS_DEFAULT_LOCATION);
    rdp_init();

    mpeg2_t mp2;
    mpeg2_open(&mp2, "rom:/2013-03-23.bDO3hZYHvwz.m1v");

    float fps = mpeg2_get_framerate(&mp2);
    throttle_init(fps, 0, 8);

    int nframes = 0;
    display_context_t disp = 0;

    while (1) {
        if (!mpeg2_next_frame(&mp2))
            break;

        RSP_WAIT_LOOP(500) {
            disp = display_lock();
            if (disp) break;
        }

        rdp_attach(disp);
        mpeg2_draw_frame(&mp2, disp);
        rdp_detach_show(disp);

        nframes++;

        int ret = throttle_wait();
        if (ret < 0) {
            debugf("videoplayer: frame %d too slow (%d Kcycles)\n", nframes, -ret);
        }

        rspq_wait();
    }
}
