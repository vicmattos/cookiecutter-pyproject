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
setup:
	make $(VENV)
	make install-req
	make clean


.PHONY: install-req
install-req: $(VENV) requirements.txt requirements-dev.txt
	$(VEXECS)/pip install -r requirements.txt
	$(VEXECS)/pip install -r requirements-dev.txt


.PHONY: clean
clean:
	$(VEXECS)/cleanpy --all --exclude-envs .


requirements.txt: pyproject.toml $(VEXECS)/pip-compile
	$(VEXECS)/pip-compile --strip-extras


requirements-dev.txt: pyproject.toml $(VEXECS)/pip-compile
	$(VEXECS)/pip-compile --strip-extras --extra=dev --output-file=requirements-dev.txt


$(VENV): $(VIRTUALENVEXEC)
	$(PY) $(VIRTUALENVEXEC) $(VENV)
	$(VEXECS)/pip install --upgrade pip


$(VIRTUALENVEXEC):
ifndef PYVERSION
	$(error Please set PYVERSION variable in Makefile)
endif
	curl https://bootstrap.pypa.io/virtualenv/$(PYVERSION)/virtualenv.pyz --output $(VIRTUALENVEXEC)


$(VEXECS)/%: $(VENV) requirements-dev.txt
	$(VEXECS)/pip install -r requirements-dev.txt
