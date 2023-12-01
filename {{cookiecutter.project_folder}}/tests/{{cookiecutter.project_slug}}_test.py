{%- if cookiecutter.command_line_interface == 'Typer' %}
from {{cookiecutter.project_slug}} import app


def test_cli_default(cli_runner):
    result = cli_runner.invoke(app)
    assert result.exit_code == 0
    output = 'Replace this message by putting your code into src/{{cookiecutter.project_slug}}.py'
    assert output in result.stdout

def test_cli_verbose(cli_runner):
    result = cli_runner.invoke(app, ["--verbose"])
    assert result.exit_code == 0
    assert 'Arguments:' in result.stdout
    result = cli_runner.invoke(app)
    assert result.exit_code == 0
    assert 'Arguments:' not in result.stdout

{%- elif cookiecutter.command_line_interface == 'Argparse' %}
from my_project import main


def test_cli_default(capsys, default_args):
    main(default_args)
    output = 'Replace this message by putting your code into src/{{cookiecutter.project_slug}}.py'
    assert output in capsys.readouterr().out

def test_cli_verbose(capsys, default_args):
    main(default_args)
    assert 'Arguments:' not in capsys.readouterr().out
    default_args.verbose = True
    main(default_args)
    assert 'Arguments:' in capsys.readouterr().out

{%- else %}
from {{cookiecutter.project_slug}} import main


def test_main(capsys):
    main()
    output = 'Replace this message by putting your code into src/{{cookiecutter.project_slug}}.py'
    assert output in capsys.readouterr().out

def test_main_verbose(capsys):
    main(verbose = True)
    message = 'Replace this message by putting your code into src/{{cookiecutter.project_slug}}.py'
    output = capsys.readouterr().out
    assert message in output
    assert 'Arguments: verbose=True' in output

{%- endif %}
