NPX := $(shell command -v npx 2> /dev/null)

LIBDRAGON_CLI_VER = 10.8.2
LIBDRAGON_CLI = $(NPX) --yes libdragon@$(LIBDRAGON_CLI_VER)

LIBDRAGON_MAKEFILE = Makefile.libdragon
LIBDRAGON_MAKE = $(LIBDRAGON_CLI) make -f $(LIBDRAGON_MAKEFILE)

OUT_Z64 := hicart.z64

.PHONY: build
build:
	$(LIBDRAGON_MAKE) all

.PHONY: clean
clean:
	$(LIBDRAGON_MAKE) clean

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
