import re
import sys


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

module_name = '{{cookiecutter.project_slug}}'

if not re.match(MODULE_REGEX, module_name):
    errmsg = f'ERROR: The project slug ({module_name}) is not a valid Python module name.'
    raise SystemExit(errmsg)
