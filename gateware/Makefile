INSTALL_STAMP := .install.stamp
PDM := $(shell command -v pdm 2> /dev/null)

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo ""
	@echo "  install     Install packages and prepare environment"
	@echo "  uninstall   Delete environement"
	@echo "  clean       Remove all temporary files"
	@echo "  program     Build design and program device"
	@echo "  test        Run all the tests"

PDM_NOT_FOUND = "PDM could not be found. See https://pdm.fming.dev/latest/"

install: $(INSTALL_STAMP)
$(INSTALL_STAMP): pyproject.toml pdm.lock
	@if [ -z $(PDM) ]; then echo $(PDM_NOT_FOUND); exit 2; fi
	$(PDM) install
	touch $(INSTALL_STAMP)

.PHONY: uninstall
uninstall:
	$(PDM) venv remove -y in-project
	rm -rf $(INSTALL_STAMP)

.PHONY: clean
clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf $(INSTALL_STAMP) build .pytest_cache

.PHONY: program
program: $(INSTALL_STAMP)
	$(PDM) run python -m hicart.design.cart

.PHONY: test
test: $(INSTALL_STAMP)
	$(PDM) run pytest
