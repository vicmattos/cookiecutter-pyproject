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


.PHONY: help
help:  ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: setup
setup:  ## Create development environment with venv and pre-commit
	make $(PYTHON)
	make pre-commit-install


.PHONY: pre-commit-install
pre-commit-install: $(VCOMMAND)/pre-commit  ## Execute pre-commit installation of script and hooks
	$(VCOMMAND)/pre-commit install --install-hooks --overwrite


.PHONY: pre-commit-run
pre-commit-run: $(VCOMMAND)/pre-commit  ## Execute `pre-commit run` in all files
	$(VCOMMAND)/pre-commit run --all-files


.PHONY: install-editable
install-editable: $(PYTHON)  ## Call pip installing local in editable mode
	$(PYTHON) -m pip install -e .


.PHONY: test
test: $(PYTHON)  ## Call pytest
	$(PYTHON) -m pytest


{%- if cookiecutter.documentation_framework == "MKDocs" %}


.PHONY: docs-build
docs-build: $(PYTHON)  ## Call mkdocs to build documentation into site/
	$(PYTHON) -m mkdocs build


.PHONY: docs-serve
docs-serve: $(PYTHON)  ## Call mkdocs to serve documentation locally
	$(PYTHON) -m mkdocs serve
{%- endif %}


.PHONY: bumpver.%
bumpver.%: $(VCOMMAND)/cz  ## Execute commitizen's `cz bump` with version scope (major, minor, patch) as suffix
	$(VCOMMAND)/cz bump --yes --files-only --increment $*


.PHONY: commit
commit: $(VCOMMAND)/cz  ## Execute commitizen's `cz commit` to create commit message and use it in `git commit`
ifeq ($(shell git diff --name-only --cached),)
	$(error Git stage empty. Add files to commit.)
endif
	$(VCOMMAND)/cz commit --dry-run --write-message-to-file .cz-msg
	git commit --file .cz-msg && rm -f .cz-msg || rm -f .cz-msg


.PHONY: clean
clean: $(PYTHON)  ## Call cleanpy skipping envs
	rm -rf site/
	$(PYTHON) -m cleanpy --all --exclude-envs .


requirements.txt: pyproject.toml $(VCOMMAND)/pip-compile  ## Execute pip-tools `pip-compile` to create requirements
	$(VCOMMAND)/pip-compile --strip-extras


requirements-dev.txt: pyproject.toml $(VCOMMAND)/pip-compile  ## Execute pip-tools `pip-compile` to create development requirements
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
