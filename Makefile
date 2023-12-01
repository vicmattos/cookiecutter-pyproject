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


.PHONY: bake-watch
bake-watch: $(VEXECS)/watchmedo
	$(VEXECS)/watchmedo shell-command \
		--command='make bake' \
		--recursive \
		\{\{cookiecutter.project_folder\}\} \
		hooks \
		cookiecutter.json


.PHONY: test
test: $(VEXECS)/pytest
	$(VEXECS)/pytest -n auto -m "not slow"


.PHONY: test-all
test-all: $(VEXECS)/pytest
	$(VEXECS)/pytest -n auto


.PHONY: docs-serve
docs-serve: $(VEXECS)/mkdocs
	$(VEXECS)/mkdocs serve


.PHONY: commit
commit: $(VEXECS)/cz
ifeq ($(shell git diff --name-only --cached),)
	$(error Git stage empty. Add files to commit.)
endif
	$(VEXECS)/cz commit --dry-run --write-message-to-file .cz-msg
	git commit --file .cz-msg && rm -f .cz-msg || rm -f .cz-msg


.PHONY: clean
clean:
	rm -rf site/
	rm -rf $(BAKE_OUTPUT)
	rm -rf .ruff_cache/
	$(VEXECS)/cleanpy --all --exclude-envs .


$(VENV):
	$(PY) -m venv $(VENV)
	$(VEXECS)/pip install --upgrade pip

$(VEXECS)/%: $(VENV)
	$(VEXECS)/pip install -r requirements-dev.txt
