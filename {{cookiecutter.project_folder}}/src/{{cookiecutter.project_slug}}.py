import argparse
from collections.abc import Sequence


def main(args) -> None:
    if args.verbose:
        print(f"Arguments: {str(args)}")
    print(f"Replace this message by putting your code into src/{{cookiecutter.project_slug}}.py")


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args(argv)
    main(args)
    return 0


if __name__ == '__main__':
    raise SystemExit(cli())