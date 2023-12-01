def test_bake_not_open_source(cookies, bake_in_temp_dir):
    with bake_in_temp_dir(
        cookies,
        extra_context={'open_source_license': 'Not open source'},
    ) as result:
        found_toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert 'LICENSE' not in found_toplevel_files
