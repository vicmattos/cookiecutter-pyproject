SYSTEM_PYTHON  = $(or $(shell which python3), $(shell which python))
PYVERSION = $(shell python -c "import sys;print(f'{sys.version_info.major}.{sys.version_info.minor}')")
VIRTUALENVEXEC = virtualenv.pyz
VENV = .venv
# make it work on windows
ifeq ($(OS), Windows_NT)
    VCOMMAND = $(VENV)/Scripts
else
	VCOMMAND = $(VENV)/bin
endif
PYTHON = $(VCOMMAND)/python


.PHONY: setup
setup: $(VCOMMAND)/pre-commit
	$(VCOMMAND)/pre-commit install --install-hooks --overwrite


.PHONY: pre-commit-run
pre-commit-run: $(VCOMMAND)/pre-commit
	$(VCOMMAND)/pre-commit run --all-files


.PHONY: install-editable
install-editable: $(PYTHON)
	$(PYTHON) -m pip install -e .


.PHONY: test
test: $(PYTHON)
	$(PYTHON) -m pytest


{%- if cookiecutter.documentation_framework == "MKDocs" %}


.PHONY: docs-build
docs-build: $(PYTHON)
	$(PYTHON) -m mkdocs build
{%- endif %}


.PHONY: bumpver.%
bumpver.%: $(VCOMMAND)/cz
	$(VCOMMAND)/cz bump --yes --files-only --increment $*


.PHONY: commit
commit: $(VCOMMAND)/cz
ifeq ($(shell git diff --name-only --cached),)
	$(error Git stage empty. Add files to commit.)
endif
	$(VCOMMAND)/cz commit --dry-run --write-message-to-file .cz-msg
	git commit --file .cz-msg && rm -f .cz-msg || rm -f .cz-msg


.PHONY: clean
clean: $(PYTHON)
	rm -rf site/
	$(PYTHON) -m cleanpy --all --exclude-envs .


requirements.txt: pyproject.toml $(VCOMMAND)/pip-compile
	$(VCOMMAND)/pip-compile --strip-extras


requirements-dev.txt: pyproject.toml $(VCOMMAND)/pip-compile
	$(VCOMMAND)/pip-compile --strip-extras --extra=dev --output-file=requirements-dev.txt


$(PYTHON): $(VENV)

$(VCOMMAND)/%:
	make $(VENV)

$(VENV): $(VIRTUALENVEXEC)
	$(SYSTEM_PYTHON) $(VIRTUALENVEXEC) $(VENV)
	$(VCOMMAND)/pip install --upgrade pip
ifeq ($(wildcard requirements-dev.txt),)  # req don't exist
	$(PYTHON) -m pip install pip-tools
	make -B requirements-dev.txt -o $(VCOMMAND)/pip-compile
endif
	$(PYTHON) -m pip install -r requirements-dev.txt

$(VIRTUALENVEXEC):
	curl https://bootstrap.pypa.io/virtualenv/$(PYVERSION)/virtualenv.pyz --output $(VIRTUALENVEXEC)
