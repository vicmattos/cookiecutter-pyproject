BAKE_OUTPUT=ouput
BAKE_OPTIONS=--no-input --output-dir $(BAKE_OUTPUT)

PY = python3
VENV = .venv
VEXECS=$(VENV)/bin

# make it work on windows
ifeq ($(OS), Windows_NT)
    VEXECS=$(VENV)/Scripts
    PY=python
endif


.PHONY: bake
bake: $(VEXECS)/cookiecutter
	$(VEXECS)/cookiecutter $(BAKE_OPTIONS) . --overwrite-if-exists


.PHONY: clean
clean:
	rm -rf $(BAKE_OUTPUT)


$(VENV):
	$(PY) -m venv $(VENV)
	$(VEXECS)/pip install --upgrade pip

$(VEXECS)/cookiecutter: $(VENV)
	$(VEXECS)/pip install cookiecutter