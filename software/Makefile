V = 0
LIBDRAGON_CLI_VER = 10.8.2
LIBDRAGON_MAKEFILE = Makefile.libdragon

NPX := $(shell command -v npx 2> /dev/null)
LIBDRAGON_CLI := $(NPX) --yes libdragon@$(LIBDRAGON_CLI_VER)
LIBDRAGON_MAKE := $(LIBDRAGON_CLI) make -f $(LIBDRAGON_MAKEFILE)

OUT_Z64 := hicart.z64

.DEFAULT_GOAL := build

.PHONY: clean
clean:
	$(LIBDRAGON_MAKE) clean

.PHONY: build
build:
	$(LIBDRAGON_MAKE) all

.PHONY: program
program: build
	ecpprog -d s:0x0403:0x6010:FT5YLSVU -I B -o 8M $(OUT_Z64)

.PHONY: emulate
emulate: build
	../scripts/run_in_ares.sh $(OUT_Z64)

.PHONY: libdragon-install
libdragon-install:
	$(LIBDRAGON_CLI) install

.PHONY: libdragon-start
libdragon-start:
	$(LIBDRAGON_CLI) start

.PHONY: libdragon-stop
libdragon-stop:
	$(LIBDRAGON_CLI) stop

ifneq ($(V),1)
.SILENT:
endif
