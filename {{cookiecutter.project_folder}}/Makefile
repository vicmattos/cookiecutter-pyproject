PYVERSION = {{ cookiecutter.python_version }}
PY = python3
VENV = .venv
VEXECS=$(VENV)/bin
VIRTUALENVEXEC = virtualenv.pyz

# make it work on windows
ifeq ($(OS), Windows_NT)
    VEXECS=$(VENV)/Scripts
    PY=python
endif


.PHONY: setup
setup: $(VEXECS)/pre-commit
	$(VEXECS)/pre-commit install --install-hooks --overwrite


.PHONY: install-editable
install-editable: $(VENV)
	$(VEXECS)/pip install -e .


.PHONY: pre-commit-run
pre-commit-run: $(VEXECS)/pre-commit
	$(VEXECS)/pre-commit run --all-files


{%- if cookiecutter.documentation_framework == "MKDocs" %}


.PHONY: docs-build
docs-build: $(VEXECS)/mkdocs
	$(VEXECS)/mkdocs build
{%- endif %}


.PHONY: commit
commit: $(VEXECS)/cz
ifeq ($(shell git diff --name-only --cached),)
	$(error Git stage empty. Add files to commit.)
endif
	$(VEXECS)/cz commit --dry-run --write-message-to-file .cz-msg
	git commit --file .cz-msg && rm -f .cz-msg || rm -f .cz-msg


.PHONY: clean
clean: $(VEXECS)/cleanpy
	rm -rf site/
	$(VEXECS)/cleanpy --all --exclude-envs .


requirements.txt: pyproject.toml $(VEXECS)/pip-compile
	$(VEXECS)/pip-compile --strip-extras


requirements-dev.txt: pyproject.toml $(VEXECS)/pip-compile
	$(VEXECS)/pip-compile --strip-extras --extra=dev --output-file=requirements-dev.txt


$(VENV): $(VIRTUALENVEXEC)
	$(PY) $(VIRTUALENVEXEC) $(VENV)
	$(VEXECS)/pip install --upgrade pip

$(VEXECS)/%: $(VENV) requirements-dev.txt
	$(VEXECS)/pip install -r requirements-dev.txt

$(VIRTUALENVEXEC):
ifndef PYVERSION
	$(error Please set PYVERSION variable in Makefile)
endif
	curl https://bootstrap.pypa.io/virtualenv/$(PYVERSION)/virtualenv.pyz --output $(VIRTUALENVEXEC)
