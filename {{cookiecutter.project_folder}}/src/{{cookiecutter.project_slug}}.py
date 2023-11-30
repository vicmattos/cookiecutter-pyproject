{%- if cookiecutter.command_line_interface == 'Typer' %}
import typer

app = typer.Typer()


@app.command()
def main(verbose: bool = False):
    if verbose:
        typer.echo(f"Arguments: {locals().keys()}")
    typer.echo("Replace this message by putting your code into src/{{cookiecutter.project_slug}}.py")


if __name__ == '__main__':
    typer.run(main)

{%- elif cookiecutter.command_line_interface == 'Argparse' %}
import argparse
from collections.abc import Sequence


class Args(argparse.Namespace):
    verbose: bool = False


def main(args: Args) -> None:
    if args.verbose:
        print(f"Arguments: {str(args)}")
    print(f"Replace this message by putting your code into src/{{cookiecutter.project_slug}}.py")


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    args: Args = parser.parse_args(argv)
    main(args)
    return 0


if __name__ == '__main__':
    raise SystemExit(cli())
{%- endif %}
