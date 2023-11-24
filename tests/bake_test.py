from pathlib import Path

import pytest


def test_bake_with_defaults(cookies, bake_in_temp_dir):
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
def test_bake_and_run_make_setup(cookies, bake_in_temp_dir, run_inside_dir):
    with bake_in_temp_dir(cookies) as result:
        run_inside_dir('git init .', result.project_path)
        assert run_inside_dir('make setup', result.project_path) == 0


def test_bake_every_python_version(cookies, bake_in_temp_dir):
    for pyversion in ['3.11', '3.10', '3.9', '3.8']:
        with bake_in_temp_dir(
            cookies,
            extra_context={'python_version': pyversion}
        ) as result:
            root: Path = result.project_path
            assert f'requires-python = ">={pyversion}' in (root / 'pyproject.toml').read_text()
            assert f'PYVERSION = {pyversion}' in (root / 'Makefile').read_text()


def test_bake_not_open_source(cookies, bake_in_temp_dir):
    with bake_in_temp_dir(
        cookies,
        extra_context={'open_source_license': 'Not open source'}
    ) as result:
        found_toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert 'LICENSE' not in found_toplevel_files
