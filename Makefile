BAKE_OUTPUT=output
BAKE_OPTIONS=--no-input --output-dir $(BAKE_OUTPUT)

PY = python3
VENV = .venv
VEXECS=$(VENV)/bin

# make it work on windows
ifeq ($(OS), Windows_NT)
    VEXECS=$(VENV)/Scripts
    PY=python
endif


.PHONY: setup
setup: $(VEXECS)/pre-commit
	$(VEXECS)/pre-commit install --install-hooks --overwrite


.PHONY: bake
bake: $(VEXECS)/cookiecutter
	$(VEXECS)/cookiecutter $(BAKE_OPTIONS) . --overwrite-if-exists


.PHONY: test
test: $(VEXECS)/pytest
	$(VEXECS)/pytest -m "not slow"


.PHONY: test-all
test-all: $(VEXECS)/pytest
	$(VEXECS)/pytest


.PHONY: docs-serve
docs-serve: $(VEXECS)/mkdocs
	$(VEXECS)/mkdocs serve


.PHONY: clean
clean:
	rm -rf site/
	rm -rf $(BAKE_OUTPUT)
	$(VEXECS)/cleanpy --all --exclude-envs .


$(VENV):
	$(PY) -m venv $(VENV)
	$(VEXECS)/pip install --upgrade pip

$(VEXECS)/%: $(VENV)
	$(VEXECS)/pip install -r requirements-dev.txt
