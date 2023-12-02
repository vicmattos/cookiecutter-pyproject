from pathlib import Path

import pytest


@pytest.mark.parametrize('pyversion', ['3.11', '3.10', '3.9', '3.8'])
def test_bake_every_python_version(cookies, bake_in_temp_dir, pyversion):
    with bake_in_temp_dir(
        cookies,
        extra_context={'python_version': pyversion},
    ) as result:
        root: Path = result.project_path
        assert f'requires-python = ">={pyversion}' in (root / 'pyproject.toml').read_text()
