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
        assert '.pre-commit-config.yaml' in found_toplevel_files


@pytest.mark.slow
def test_bake_and_run_make_setup(cookies, bake_in_temp_dir, run_inside_dir):
    with bake_in_temp_dir(cookies) as result:
        run_inside_dir('git init .', result.project_path)
        assert run_inside_dir('make setup', result.project_path) == 0


@pytest.mark.parametrize('pyversion', ['3.11', '3.10', '3.9', '3.8'])
def test_bake_every_python_version(cookies, bake_in_temp_dir, pyversion):
    with bake_in_temp_dir(
        cookies,
        extra_context={'python_version': pyversion},
    ) as result:
        root: Path = result.project_path
        assert f'requires-python = ">={pyversion}' in (root / 'pyproject.toml').read_text()
        assert f'PYVERSION = {pyversion}' in (root / 'Makefile').read_text()


def test_bake_not_open_source(cookies, bake_in_temp_dir):
    with bake_in_temp_dir(
        cookies,
        extra_context={'open_source_license': 'Not open source'},
    ) as result:
        found_toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert 'LICENSE' not in found_toplevel_files


@pytest.mark.slow
def test_bake_and_run_make_docs_build(cookies, bake_in_temp_dir, run_inside_dir):
    with bake_in_temp_dir(cookies) as result:
        assert run_inside_dir('make docs-build', result.project_path) == 0
        assert 'site' in [f.name for f in result.project_path.iterdir()]


def test_bake_no_docs_framework(cookies, bake_in_temp_dir, text_in_file):
    with bake_in_temp_dir(
        cookies,
        extra_context={'documentation_framework': 'No documentation'},
    ) as result:
        found_toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert 'mkdocs.yml' not in found_toplevel_files
        assert 'docs/' not in found_toplevel_files

        pyproject_toml = result.project_path / 'pyproject.toml'
        assert text_in_file('mkdocs-material', pyproject_toml, negate=True)

        makefile = result.project_path / 'Makefile'
        assert text_in_file('mkdocs', makefile, negate=True)

        gh_workflow = result.project_path / '.github' / 'workflows' / 'docs.yml'
        assert not gh_workflow.exists()


@pytest.mark.slow
@pytest.mark.parametrize('cli_tool', ['Typer', 'Argparse'])
def test_bake_with_cli_package(cookies, bake_in_temp_dir, cli_tool, run_inside_dir):
    with bake_in_temp_dir(
        cookies,
        extra_context={
            'project_folder': 'pkg_command',
            'command_line_interface': cli_tool,
        },
    ) as result:
        assert run_inside_dir('make install-editable', result.project_path) == 0
        assert run_inside_dir('.venv/bin/pkg_command --help', result.project_path) == 0


@pytest.mark.parametrize('cli_tool', ['Typer', 'Argparse'])
def test_bake_with_callable_cli(cookies, bake_in_temp_dir, cli_tool, run_inside_dir):
    with bake_in_temp_dir(
        cookies,
        extra_context={
            'project_slug': 'pkg_command',
            'command_line_interface': cli_tool,
        },
    ) as result:
        assert run_inside_dir('python src/pkg_command.py --help', result.project_path) == 0


@pytest.mark.slow
def test_run_pre_commit(cookies, bake_in_temp_dir, run_inside_dir):
    with bake_in_temp_dir(cookies) as result:
        run_inside_dir('git init .', result.project_path)
        assert run_inside_dir('make pre-commit-run', result.project_path) == 0


@pytest.mark.parametrize(
    ('cli_tool', 'is_not_present'),
    [
        ('Typer', False),
        ('Argparse', True),
        ('No command-line interface', True),
    ]
)
def test_bake_cli_typer_as_dependency(cookies, bake_in_temp_dir, text_in_file, cli_tool, is_not_present):
    with bake_in_temp_dir(
        cookies,
        extra_context={
            'project_slug': 'project_slug',
            'command_line_interface': cli_tool
        }
    ) as result:
        pyproject_toml = result.project_path / 'pyproject.toml'
        assert text_in_file('typer', pyproject_toml, negate=is_not_present)
        source_code = result.project_path / 'src' / 'project_slug.py'
        assert text_in_file('typer', source_code, negate=is_not_present)
