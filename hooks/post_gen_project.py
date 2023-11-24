from pathlib import Path


if __name__ == "__main__":

    if '{{cookiecutter.open_source_license}}' == 'Not open source':
        Path("LICENSE").unlink()
