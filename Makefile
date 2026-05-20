PYTHON = $(if $(wildcard $(VENV_PYTHON)), $(VENV_PYTHON), python3)
PIP = $(if $(wildcard $(VENV_PIP)), $(VENV_PIP), pip)
MYPY_FLAGS= --warn-return-any --warn-unused-ignores --ignore-missing-imports \
			--disallow-untyped-defs --check-untyped-defs


define step
	@printf "$(1)"; \
	out="$$( { $(2); } 2>&1 )"; \
	status="$$?"; \
	if [ "$$status" -eq 0 ]; then \
		printf "$(GREEN) $(1) $(RESET)\n"; \
	else \
		printf "$(RED) $(1) $(RESET)\n"; \
		printf "\n$$out\n\n"; \
		exit $$status; \
	fi
endef

install:
	$(call step,Installing all required packages,$(PIP) install -r requirements.txt)
	$(call step,Installing mazegenerator,$(PIP) install mazegenerator-00001-py3-none-any.whl)

clean:
				@echo "$(RED) Cleaning...$(RESET)"
				@find . -type d -name "__pycache__" -exec rm -rf {} +
				@find . -type f -name "*.pyc" -delete
				@rm -rf .mypy_cache
				@rm -rf .pytest_cache
				@rm -rf .coverage

lint:
	$(call step,Looking for flake8 error,$(PYTHON) -m flake8 .)
	$(call step,Looking for mypy error,$(PYTHON) -m mypy . $(MYPY_FLAGS))

lint-strict:
	$(call step,Looking for flake8 error,$(PYTHON) -m flake8 .)
	$(call step,Looking for mypy strict error,$(PYTHON) -m mypy . --strict --ignore-missing-imports)

run:
	@$(PYTHON) main.py config.json

debug:
	@$(PYTHON) -m pdb main.py config.json

venv:
				@echo "$(BLUE)Create virtual environment$(RESET)"
				@$(PYTHON) -m venv .venv
				@echo "$(BLUE)Run 'source .venv/bin/activate' to go to the virtual environment."

build:
	$(call step,Building the project,pyinstaller main.py --onefile --name pac-man --add-data "sprite:sprite" --add-data "sounds:sounds" --add-data "font:font")
	$(call step,Copying sprites,cp -r sprite dist)
	$(call step,Copying sounds,cp -r sounds dist)
	$(call step,Copying font,cp -r font dist)
	$(call step,Copying user manual, cp user_manual.txt dist/README.md)
	$(call step,Copying default config,cp config.json dist/config.json)
	$(call step,Creating default highscore file, cd dist && touch highscorers.json && cd ../)
	$(call step,Zipping the project,cd dist && zip pac-man.zip ./* -r && mv ./pac-man.zip ../pac-man.zip)

all: run


.PHONY: run all debug venv lint lint-strict clean install


RESET=\033[0m
RED=\033[1;31m
BLUE=\033[1;34m
GREEN=\033[1;32m
YELLOW=\033[1;33m