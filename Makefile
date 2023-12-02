SYSTEM_PYTHON  = $(or $(shell which python3), $(shell which python))
VENV = .venv
# make it work on windows
ifeq ($(OS), Windows_NT)
    VEXECS = $(VENV)/Scripts
else
	VEXECS = $(VENV)/bin
endif
PYTHON = $(VEXECS)/python


.PHONY: setup
setup: $(VEXECS)
	$(VEXECS)/pre-commit install --install-hooks --overwrite


.PHONY: bake
BAKE_OUTPUT=output
bake: $(PYTHON)
	$(PYTHON) -m cookiecutter . --no-input --output-dir $(BAKE_OUTPUT) --overwrite-if-exists


.PHONY: bake-watch
bake-watch: $(VEXECS)
	$(VEXECS)/watchmedo shell-command \
		--command='make bake' \
		--recursive \
		\{\{cookiecutter.project_folder\}\} \
		hooks \
		cookiecutter.json


.PHONY: test
test: $(PYTHON)
	$(PYTHON) -m pytest -n auto -m "not slow"


.PHONY: test-all
test-all: $(PYTHON)
	$(PYTHON) -m pytest -n auto


.PHONY: docs-serve
docs-serve: $(PYTHON)
	$(PYTHON) -m mkdocs serve


.PHONY: commit
commit: $(VEXECS)
ifeq ($(shell git diff --name-only --cached),)
	$(error Git stage empty. Add files to commit.)
endif
	$(VEXECS)/cz commit --dry-run --write-message-to-file .cz-msg
	git commit --file .cz-msg && rm -f .cz-msg || rm -f .cz-msg


.PHONY: clean
clean: $(PYTHON)
	rm -rf site/
	rm -rf $(BAKE_OUTPUT)
	rm -rf .ruff_cache/
	$(PYTHON) -m cleanpy --all --exclude-envs .


$(PYTHON):
	$(SYSTEM_PYTHON) -m venv $(VENV)
	$(VEXECS)/pip install --upgrade pip
	$(VEXECS)/pip install -r requirements-dev.txt

$(VEXECS): $(PYTHON)
