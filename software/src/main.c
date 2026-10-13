#include <stdio.h>
#include <libdragon.h>

#include <n64sys.h>
#include <video.h>
#include <video_sync.h>
#include <yuv.h>
#include <display.h>
#include <vi.h>
#include <wav64.h>
#include <mixer.h>
#include <graphics.h>
#include <rdpq.h>
#include <rdpq_attach.h>

#include "sdhi.h"
#include "soak.h"

void hi_video_play(const char *video_fn, bool loop);

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

	dfs_init(DFS_DEFAULT_LOCATION);
    sdhi_init();

	rdpq_init();
	yuv_init();
	joypad_init();

	audio_init(AUDIO_HZ, 4);
	mixer_init(8);

	video_register_codec(&mpeg1_codec);
	video_register_codec(&h264_codec);

	display_init(RESOLUTION_320x240, DEPTH_32_BPP, 2, GAMMA_NONE, FILTERS_RESAMPLE);

	hi_video_play("sdhi:/2013-06-21.huXPjbKqlra.m1v", true);
}

void hi_video_play(const char *video_fn, bool loop)
{
    int buffered_pics = 4;
    video_t *video = video_open(video_fn, &(video_parms_t){ .buffered_pics = buffered_pics });
    video_info_t info = video_get_info(video);

    bool vi_16bpp = display_get_bitdepth() == 2;

    yuv_init();
    yuv_blitter_t yuv;
	yuv = yuv_blitter_new_fmv(
		info.width, info.height,
		display_get_width(), display_get_height(),
		&(yuv_fmv_parms_t){
			.cs = &info.colorspace,
			.video_aspect_ratio = info.aspect_ratio,
			.display_aspect_ratio = vi_get_aspect_ratio(),
			.enable_dithering = vi_16bpp, // YUV blitter will dither in 16bpp mode
		}
	);

    // Engage the fps limiter to ensure proper video pacing.
    display_set_fps_limit(info.framerate);

	// Try to find audio file with same name but .wav64 extension
	const char *ext = strrchr(video_fn, '.');
	assertf(ext, "Audio filename not specified for video playback");
	// Create audio filename
	const char *audio_fn = alloca(strlen(video_fn) + 7);
	size_t base_len = ext - video_fn;
	strncpy((char*)audio_fn, video_fn, base_len);
	strcpy((char*)audio_fn + base_len, ".wav64");

	// Load audio
    wav64_t* audio = wav64_load(audio_fn, NULL);

    int frame_idx = 0;
    bool abort = false;

	mixer_ch_play(0, &audio->wave);
    video_sync_t *vsync = video_sync_create(video, NULL);

    while (!abort) {
        bool skip_render = false;

        mixer_try_play();

		if (mixer_ch_playing(0)) {
			// Decide what to do next based on the sync controller
			double master_time_sec = mixer_ch_get_pos(0) / (double)audio->wave.frequency;
			video_sync_action_t a = video_sync_step(vsync, master_time_sec, frame_idx);

			if (a.kind == VIDEO_SYNC_SKIP_NEXT) {
				// Skip rendering this frame
				skip_render = true;
			} else if (a.kind == VIDEO_SYNC_SEEK_AND_RENDER) {
				// Seek to the target frame and render it.
				int new_idx = video_seek(video, a.seek_frame);
				if (new_idx >= 0) {
					frame_idx = new_idx;
				}
			}
		}

		if (!video_next_frame(video)) {
			if (loop) {
				frame_idx = 0;
				video_rewind(video);
				mixer_ch_stop(0);
				mixer_ch_play(0, &audio->wave);
				video_sync_reset(vsync, frame_idx);
				continue;
			} else {
				break;
			}
		}

        mixer_try_play();

        if (!skip_render) {
            surface_t *disp = display_try_get();
            while (disp == NULL) {
                if (!video_poll(video)) {
                    disp = display_get();
                    break;
                }
                disp = display_try_get();
            }

            rdpq_attach(disp, NULL);

            // Get the next video frame and feed it into our previously set up blitter.
            yuv_frame_t frame = video_get_frame(video);
            yuv_blitter_run(&yuv, &frame);

            rdpq_detach_show();
        }

        frame_idx++;
    }

    rspq_wait();

	mixer_ch_stop(0);
	wav64_close(audio);

    yuv_blitter_free(&yuv);
    yuv_close();

    video_sync_destroy(vsync);
    video_close(video);

    display_set_fps_limit(0);
}
