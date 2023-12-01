import pytest


@pytest.mark.slow
def test_bake_and_run_make_docs_build(cookies, bake_in_temp_dir, run_inside_dir):
    with bake_in_temp_dir(cookies) as result:
        assert run_inside_dir('make docs-build', result.project_path) == 0
        assert 'site' in [f.name for f in result.project_path.iterdir()]


def test_bake_no_docs_framework(cookies, bake_in_temp_dir, text_in_file):
    with bake_in_temp_dir(
        cookies,
        extra_context={
            'documentation_framework': 'No documentation',
            'github_username': 'gh_user',
            'project_folder': 'some_folder',
        },
    ) as result:
        found_toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert 'mkdocs.yml' not in found_toplevel_files
        assert 'docs/' not in found_toplevel_files

        pyproject_toml = result.project_path / 'pyproject.toml'
        assert text_in_file('mkdocs-material', pyproject_toml, not_in=True)
        assert text_in_file('mkdocs-material', pyproject_toml, not_in=True)
        assert text_in_file('https://gh_user.github.io/some_folder', pyproject_toml, not_in=True)

        makefile = result.project_path / 'Makefile'
        assert text_in_file('mkdocs', makefile, not_in=True)

        gh_workflow = result.project_path / '.github' / 'workflows' / 'docs.yml'
        assert not gh_workflow.exists()
