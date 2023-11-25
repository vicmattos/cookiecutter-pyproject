from pathlib import Path
from shutil import rmtree
import tomli
import tomli_w


if __name__ == "__main__":

    if '{{cookiecutter.open_source_license}}' == 'Not open source':
        Path("LICENSE").unlink()

    if '{{cookiecutter.documentation_framework}}' == 'No documentation':
        Path("mkdocs.yml").unlink()
        rmtree("docs/")
        with open('pyproject.toml', 'rb') as f:
            pytoml = tomli.load(f)
        pytoml['project']['optional-dependencies']['dev'].remove("mkdocs-material")
        with open('pyproject.toml', 'wb') as f:
            tomli_w.dump(pytoml, f)
