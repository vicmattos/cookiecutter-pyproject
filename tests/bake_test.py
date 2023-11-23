from contextlib import contextmanager
from pathlib import Path
import os
import subprocess
import shlex

import pytest
from cookiecutter.utils import rmtree

@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project_path))


def run_inside_dir(command: str, dirpath: Path) -> int:
    """
    Run a command from inside a given directory, returning the exit status
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        ret = subprocess.check_call(shlex.split(command))
    finally:
        os.chdir(old_path)
    return ret


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project_path.is_dir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert '.editorconfig' in found_toplevel_files
        assert '.gitignore' in found_toplevel_files
        assert 'Makefile' in found_toplevel_files
        assert 'pyproject.toml' in found_toplevel_files


@pytest.mark.slow
def test_bake_and_run_make_setup(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project_path.is_dir()
        run_inside_dir('make setup', str(result.project_path)) == 0


def test_bake_every_python_version(cookies):
    for pyversion in ['3.11', '3.10', '3.9', '3.8']:
        with bake_in_temp_dir(
            cookies,
            extra_context={'python_version': pyversion}
        ) as result:
            root: Path = result.project_path
            assert f'requires-python = ">={pyversion}' in (root / 'pyproject.toml').read_text()
            assert f'PYVERSION = {pyversion}' in (root / 'Makefile').read_text()
