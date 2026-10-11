#include <stdio.h>
#include <libdragon.h>
#include "sdhi.h"
#include "soak.h"

// Maximum target audio frequency.
//
// Needs to be 48 kHz if Opus audio compression is used.
// In this example, we are using VADPCM audio compression
// which means we can use the real frequency of the audio track.
#define AUDIO_HZ 32000.0f

int main(void)
{
    debug_init_emulog();
    debug_init_usblog();

    sdhi_init();

	dfs_init(DFS_DEFAULT_LOCATION);
	rdpq_init();
	yuv_init();
	joypad_init();

	audio_init(AUDIO_HZ, 4);
	mixer_init(8);

	video_register_codec(&mpeg1_codec);
	video_register_codec(&h264_codec);

    while (1) {
        fmv_play("sdhi:/2013-06-21.huXPjbKqlra.m1v", &(fmv_parms_t) {

        });
    }
}
