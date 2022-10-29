INSTALL_STAMP := .install.stamp
POETRY := $(shell command -v poetry 2> /dev/null)

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

POETRY_NOT_FOUND = "Poetry could not be found. See https://python-poetry.org/docs/"

install: $(INSTALL_STAMP)
$(INSTALL_STAMP): pyproject.toml poetry.lock
	@if [ -z $(POETRY) ]; then echo $(POETRY_NOT_FOUND); exit 2; fi
	$(POETRY) install
	touch $(INSTALL_STAMP)

.PHONY: uninstall
uninstall:
	$(POETRY) env remove --all
	rm -rf $(INSTALL_STAMP)

.PHONY: clean
clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf $(INSTALL_STAMP) build .pytest_cache

.PHONY: program
program: $(INSTALL_STAMP)
	$(POETRY) run python -m hicart.design.cart

.PHONY: test
test: $(INSTALL_STAMP)
	$(POETRY) run pytest

