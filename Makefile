MYPY_FLAGS= --warn-return-any --warn-unused-ignores --ignore-missing-imports \
			--disallow-untyped-defs --check-untyped-defs



clean:
				@echo "$(RED) Cleaning...$(RESET)"
				@find . -type d -name "__pycache__" -exec rm -rf {} +
				@find . -type f -name "*.pyc" -delete
				@rm -rf .mypy_cache
				@rm -rf .pytest_cache
				@rm -rf .coverage

lint:
	@echo "$(RED)Searching for norm error...$(RESET)"
	@python3 -m flake8 .
	@python3 -m mypy . $(MYPY_FLAGS)

lint-strict:
	@echo "$(RED)Searching for severe norm error...$(RESET)"
	@python3 -m flake8 .
	@python3 -m mypy . --strict

run:
	@python3 main.py config.json

debug:
	@python3 -m pdb main.py config.json

venv:
				@echo "$(BLUE)Create virtual environment$(RESET)"
				@python3 -m venv .venv
				@echo "$(BLUE)Run 'source .venv/bin/activate' to go to the virtual environment."

all: run


RESET=\033[0m
RED=\033[1;31m
BLUE=\033[1;34m
GREEN=\033[1;32m
YELLOW=\033[1;33m