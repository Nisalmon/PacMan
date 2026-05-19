PYTHON = $(if $(wildcard $(VENV_PYTHON)), $(VENV_PYTHON), python3)
PIP = $(if $(wildcard $(VENV_PIP)), $(VENV_PIP), pip)
MYPY_FLAGS= --warn-return-any --warn-unused-ignores --ignore-missing-imports \
			--disallow-untyped-defs --check-untyped-defs


install:
	@$(PIP) install requierements.txt

clean:
				@echo "$(RED) Cleaning...$(RESET)"
				@find . -type d -name "__pycache__" -exec rm -rf {} +
				@find . -type f -name "*.pyc" -delete
				@rm -rf .mypy_cache
				@rm -rf .pytest_cache
				@rm -rf .coverage

lint:
	@echo "$(RED)Searching for norm error...$(RESET)"
	@$(PYTHON) -m flake8 .
	@$(PYTHON) -m mypy . $(MYPY_FLAGS)

lint-strict:
	@echo "$(RED)Searching for severe norm error...$(RESET)"
	@$(PYTHON) -m flake8 .
	@$(PYTHON) -m mypy . --strict

run:
	@$(PYTHON) main.py config.json

debug:
	@$(PYTHON) -m pdb main.py config.json

venv:
				@echo "$(BLUE)Create virtual environment$(RESET)"
				@$(PYTHON) -m venv .venv
				@echo "$(BLUE)Run 'source .venv/bin/activate' to go to the virtual environment."

all: run


.PHONY: run all debug venv lint lint-strict clean install


RESET=\033[0m
RED=\033[1;31m
BLUE=\033[1;34m
GREEN=\033[1;32m
YELLOW=\033[1;33m