INSTALL_STAMP := .install.stamp
PDM := $(shell command -v pdm 2> /dev/null)

PACKAGE_ROOT := src/hicart
SRCS := $(shell find $(PACKAGE_ROOT) -name "*.py")
BITSTREAM := build/top.bit

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo ""
	@echo "  install    Install packages and prepare environment"
	@echo "  uninstall  Delete environement"
	@echo "  clean      Remove all temporary files"
	@echo "  build      Build design"
	@echo "  send       Send bitstream to device"
	@echo "  program    Write bitstream to flash"
	@echo "  run        Send bitstream to device and cycle power"
	@echo "  test       Run all the tests"

PDM_NOT_FOUND = "PDM could not be found. See https://pdm.fming.dev/latest/"

install: $(INSTALL_STAMP)
$(INSTALL_STAMP): pyproject.toml pdm.lock
	@if [ -z $(PDM) ]; then echo $(PDM_NOT_FOUND); exit 2; fi
	$(PDM) install
	touch $(INSTALL_STAMP)

.PHONY: uninstall
uninstall:
	$(PDM) venv remove -y in-project
	rm -rf .pdm-build
	rm -rf $(INSTALL_STAMP)

.PHONY: clean
clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf $(INSTALL_STAMP) build .pytest_cache

.PHONY: build
build: $(BITSTREAM)

.PHONY: send
send: $(BITSTREAM)
	ecpprog -d s:0x0403:0x6010:FT5YLSVU -I B -S $(BITSTREAM)

.PHONY: program
program: $(BITSTREAM)
	ecpprog -d s:0x0403:0x6010:FT5YLSVU -I B $(BITSTREAM)

.PHONY: run
run: send
	../scripts/set_power_state.sh --silent --state 0
	../scripts/set_power_state.sh --silent --state 1

.PHONY: test
test: $(INSTALL_STAMP)
	$(PDM) run pytest

$(BITSTREAM): $(INSTALL_STAMP) $(SRCS) ../firmware/firmware.bin
	$(PDM) run python -m hicart.design.cart

../firmware/firmware.bin:
	$(MAKE) -C ../firmware