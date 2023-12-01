import pytest


def test_bake_with_defaults(cookies, bake_in_temp_dir, text_in_file):
    with bake_in_temp_dir(cookies) as result:
        assert result.project_path.is_dir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert '.cz.toml' in found_toplevel_files
        assert '.editorconfig' in found_toplevel_files
        assert '.gitignore' in found_toplevel_files
        assert '.pre-commit-config.yaml' in found_toplevel_files
        assert 'Makefile' in found_toplevel_files
        assert 'pyproject.toml' in found_toplevel_files
        assert 'requirements-dev.txt' in found_toplevel_files

        requirements_dev = result.project_path / 'requirements-dev.txt'
        text_in_file('pip-tools\\n', requirements_dev)


@pytest.mark.slow
def test_bake_and_run_make_setup(cookies, bake_in_temp_dir, run_inside_dir):
    with bake_in_temp_dir(cookies) as result:
        run_inside_dir('git init .', result.project_path)
        assert run_inside_dir('make setup', result.project_path) == 0


@pytest.mark.slow
def test_run_pre_commit(cookies, bake_in_temp_dir, run_inside_dir):
    with bake_in_temp_dir(cookies) as result:
        run_inside_dir('git init .', result.project_path)
        assert run_inside_dir('make pre-commit-run', result.project_path) == 0


@pytest.mark.slow
def test_run_bump_version(cookies, bake_in_temp_dir, run_inside_dir, text_in_file):
    with bake_in_temp_dir(cookies) as result:
        run_inside_dir('git init .', result.project_path)
        run_inside_dir('git commit --no-verify --allow-empty -m "first"', result.project_path)
        pyproject_toml = result.project_path / 'pyproject.toml'

        assert run_inside_dir('make bumpver.patch', result.project_path) == 0
        assert text_in_file('version = "0.0.2"', pyproject_toml)
        assert run_inside_dir('make bumpver.minor', result.project_path) == 0
        assert text_in_file('version = "0.1.0"', pyproject_toml)
        assert run_inside_dir('make bumpver.major', result.project_path) == 0
        assert text_in_file('version = "1.0.0"', pyproject_toml)
