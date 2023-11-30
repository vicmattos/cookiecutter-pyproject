import pytest
{%- if cookiecutter.command_line_interface == 'Typer' %}
from typer.testing import CliRunner


@pytest.fixture
def cli_runner():
    return CliRunner()

{%- elif cookiecutter.command_line_interface == 'Argparse' %}

from {{cookiecutter.project_slug}} import Args


@pytest.fixture
def default_args():
    return Args(
        verbose = False
    )

{%- endif %}
