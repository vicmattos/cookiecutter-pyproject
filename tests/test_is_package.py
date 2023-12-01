def test_is_package(cookies, bake_in_temp_dir, text_in_file):
    with bake_in_temp_dir(cookies, extra_context={'is_package': False}) as result:
        found_toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert 'src/' not in found_toplevel_files
        pyproject_toml = result.project_path / 'pyproject.toml'
        assert text_in_file('src', pyproject_toml, not_in=True)
