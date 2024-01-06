SYSTEM_PYTHON  = $(or $(shell which python3), $(shell which python))
PYVERSION = $(shell python -c "import sys;print(f'{sys.version_info.major}.{sys.version_info.minor}')")
VIRTUALENVEXEC = virtualenv.pyz
VENV = .venv
# make it work on windows
ifeq ($(OS), Windows_NT)
    VENV_EXEC = $(VENV)/Scripts
else
	VENV_EXEC = $(VENV)/bin
endif
PYTHON = $(VENV_EXEC)/python


.PHONY: help
help:  ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: setup
setup:  ## Create development environment with venv and pre-commit
	make $(PYTHON)
	make pre-commit-install


.PHONY: pre-commit-install
pre-commit-install: $(VENV_EXEC)/pre-commit  ## Execute pre-commit installation of script and hooks
	$(VENV_EXEC)/pre-commit install --install-hooks --overwrite


.PHONY: pre-commit-run
pre-commit-run: $(VENV_EXEC)/pre-commit  ## Execute `pre-commit run` in all files
	$(VENV_EXEC)/pre-commit run --all-files


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
bumpver.%: $(VENV_EXEC)/cz  ## Execute commitizen's `cz bump` with version scope (major, minor, patch) as suffix
	$(VENV_EXEC)/cz bump --yes --files-only --increment $*


.PHONY: commit
commit: $(VENV_EXEC)/cz  ## Execute commitizen's `cz commit` to create commit message and use it in `git commit`
ifeq ($(shell git diff --name-only --cached),)
	$(error Git stage empty. Add files to commit.)
endif
	$(VENV_EXEC)/cz commit --dry-run --write-message-to-file .cz-msg
	git commit --file .cz-msg && rm -f .cz-msg || rm -f .cz-msg


.PHONY: clean
clean: $(PYTHON)  ## Call cleanpy skipping envs
	$(PYTHON) -m cleanpy --all --exclude-envs .
ifeq ($(OS), Windows_NT)
	rd /s/q site/
else
	rm -rf site/
endif


requirements.txt: pyproject.toml $(VENV_EXEC)/pip-compile  ## Execute pip-tools `pip-compile` to create requirements
	$(VENV_EXEC)/pip-compile --strip-extras


requirements-dev.txt: pyproject.toml $(VENV_EXEC)/pip-compile  ## Execute pip-tools `pip-compile` to create development requirements
	$(VENV_EXEC)/pip-compile --strip-extras --extra=dev --output-file=requirements-dev.txt


$(PYTHON): $(VENV)

$(VENV_EXEC)/%: $(VENV)

$(VENV): $(VIRTUALENVEXEC)
	$(SYSTEM_PYTHON) $(VIRTUALENVEXEC) $(VENV)
	$(VENV_EXEC)/pip install --upgrade pip
ifeq ($(wildcard requirements-dev.txt),)  # req don't exist
	$(PYTHON) -m pip install pip-tools
	make -B requirements-dev.txt -o $(VENV_EXEC)/pip-compile
endif
	$(PYTHON) -m pip install -r requirements-dev.txt

$(VIRTUALENVEXEC):
	curl https://bootstrap.pypa.io/virtualenv/$(PYVERSION)/virtualenv.pyz --output $(VIRTUALENVEXEC)
