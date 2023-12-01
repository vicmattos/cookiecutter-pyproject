import pytest


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


def test_bake_with_callable_argparse(cookies, bake_in_temp_dir, run_inside_dir):
    with bake_in_temp_dir(
        cookies,
        extra_context={
            'project_slug': 'pkg_command',
            'command_line_interface': 'Argparse',
        },
    ) as result:
        assert run_inside_dir('python src/pkg_command.py --help', result.project_path) == 0


@pytest.mark.parametrize(
    ('cli_tool', 'is_not_present'),
    [
        ('Typer', False),
        ('Argparse', True),
        ('No command-line interface', True),
    ],
)
def test_bake_cli_typer_as_dependency(
    cookies, bake_in_temp_dir, text_in_file, cli_tool, is_not_present
):
    with bake_in_temp_dir(
        cookies, extra_context={'project_slug': 'project_slug', 'command_line_interface': cli_tool}
    ) as result:
        pyproject_toml = result.project_path / 'pyproject.toml'
        assert text_in_file('typer', pyproject_toml, not_in=is_not_present)
        source_code = result.project_path / 'src' / 'project_slug.py'
        assert text_in_file('typer', source_code, not_in=is_not_present)


@pytest.mark.slow
@pytest.mark.parametrize('cli_tool', ['Typer', 'Argparse'])
def test_bake_test_cli(cookies, bake_in_temp_dir, cli_tool, run_inside_dir):
    with bake_in_temp_dir(
        cookies,
        extra_context={
            'command_line_interface': cli_tool,
        },
    ) as result:
        assert run_inside_dir('make test', result.project_path) == 0
