V = 0

FFMPEG := $(shell command -v ffmpeg 2> /dev/null)

# Video
FFMPEG_FLAGS := -c:v mpeg1video -b:v 30000
FFMPEG_FLAGS += -vf scale=256:240:flags=lanczos

# Audio
# FFMPEG_FLAGS += -c:a mp2
FFMPEG_FLAGS += -an

SRC_DIR := vines/output/video/high
DST_DIR := build

SRC_SUFFIX := mp4
DST_SUFFIX := m1v

SRCS = $(wildcard $(SRC_DIR)/*.$(SRC_SUFFIX))
DSTS = $(SRCS:$(SRC_DIR)/%.$(SRC_SUFFIX)=$(DST_DIR)/%.$(DST_SUFFIX))

.PHONY: all
all: $(DSTS)

.PHONY: clean
clean:
	rm -rf $(DST_DIR)

$(DST_DIR)/%.$(DST_SUFFIX): $(SRC_DIR)/%.$(SRC_SUFFIX)
	mkdir -p $(DST_DIR)
	@echo "    [FFMPEG] $(notdir $<) => $@"
	$(FFMPEG) -threads 1 -i $< $(FFMPEG_FLAGS) $@

ifneq ($(V),1)
FFMPEG_FLAGS += -loglevel quiet
.SILENT:
endif
