from __future__ import annotations
from pathlib import Path
from shutil import rmtree


if __name__ == "__main__":

    if '{{cookiecutter.open_source_license}}' == 'Not open source':
        Path("LICENSE").unlink()

    if '{{cookiecutter.documentation_framework}}' == 'No documentation':
        rmtree("docs/")
        Path("mkdocs.yml").unlink()
        Path(".github/workflows/docs.yml").unlink()
