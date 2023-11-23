import re
import sys


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

module_name = '{{cookiecutter.project_slug}}'
license_pick = '{{cookiecutter.project_slug}}'
full_name = '{{cookiecutter.full_name}}'

if not re.match(MODULE_REGEX, module_name):
    errmsg = f'ERROR: The project slug ({module_name}) is not a valid Python module name.'
    raise SystemExit(errmsg)

if (license_pick is 'Not open source' and len(full_name) == 0):
    errmsg = f'ERROR: License {license_pick} requires your full name.'
    raise SystemExit(errmsg)
