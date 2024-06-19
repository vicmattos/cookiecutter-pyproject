from __future__ import annotations
from pathlib import Path
from shutil import rmtree


if '{{cookiecutter.open_source_license}}' == 'Not open source':
    Path('LICENSE').unlink()

if '{{cookiecutter.documentation_framework}}' == 'No documentation':
    rmtree('docs/')
    Path('mkdocs.yml').unlink()
    Path('.github/workflows/docs.yml').unlink()

if not {{cookiecutter.is_package}}:  # noqa: F821
    rmtree('src/')
    rmtree('tests/')
