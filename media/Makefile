FFMPEG := $(shell command -v ffmpeg 2> /dev/null)

FFMPEG_FLAGS := -vcodec mpeg1video
FFMPEG_FLAGS += -acodec mp2
FFMPEG_FLAGS += -vf scale=240:240:flags=lanczos

SRC_DIR := vines/output/video/high
DST_DIR := build

SRCS = $(wildcard $(SRC_DIR)/*.mp4)
DSTS = $(SRCS:$(SRC_DIR)/%.mp4=$(DST_DIR)/%.mpg)

.PHONY: all
all: $(DSTS)

.PHONY: clean
clean:
	rm -rf $(DST_DIR)

$(DST_DIR)/%.mpg: $(SRC_DIR)/%.mp4
	mkdir -p $(DST_DIR)
	$(FFMPEG) -threads 1 -i $< $(FFMPEG_FLAGS) $@
