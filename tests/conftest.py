
from contextlib import contextmanager
from pathlib import Path
import os
import subprocess
import shlex

import pytest
from cookiecutter.utils import rmtree

@pytest.fixture
def bake_in_temp_dir():
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
    return bake_in_temp_dir


@pytest.fixture
def run_inside_dir():
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
    return run_inside_dir
