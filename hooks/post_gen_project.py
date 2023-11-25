from __future__ import annotations
from pathlib import Path
from shutil import rmtree
import tomli
import tomli_w


def toml_handler(filepath: Path) -> tuple[dict, callable]:
    with open(filepath, 'rb') as f:
        config = tomli.load(f)
    def writer(config):
        with open(filepath, 'wb') as f:
            tomli_w.dump(pytoml, f)
    return config, writer



if __name__ == "__main__":

    if '{{cookiecutter.open_source_license}}' == 'Not open source':
        Path("LICENSE").unlink()

    if '{{cookiecutter.documentation_framework}}' == 'No documentation':
        rmtree("docs/")
        Path("mkdocs.yml").unlink()
        pytoml, writer = toml_handler(Path('pyproject.toml'))
        writer(pytoml['project']['optional-dependencies']['dev'].remove("mkdocs-material"))
