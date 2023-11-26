from __future__ import annotations
from pathlib import Path
from shutil import rmtree
import tomlkit


def toml_handler(filepath: Path) -> tuple[dict, callable]:
    with open(filepath, 'rt') as f:
        config = tomlkit.load(f)
    def writer(config):
        with open(filepath, 'wt') as f:
            tomlkit.dump(pytoml, f)
    return config, writer



if __name__ == "__main__":

    if '{{cookiecutter.open_source_license}}' == 'Not open source':
        Path("LICENSE").unlink()

    if '{{cookiecutter.documentation_framework}}' == 'No documentation':
        rmtree("docs/")
        Path("mkdocs.yml").unlink()
        Path(".github/workflows/docs.yml").unlink()
        pytoml, writer = toml_handler(Path('pyproject.toml'))
        writer(pytoml['project']['optional-dependencies']['dev'].remove("mkdocs-material"))
