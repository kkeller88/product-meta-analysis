import os
from pathlib import Path
import re

import yaml


CONFIG_DIR = os.path.join(Path(__file__).parents[2], 'config')


def read_config(folder, name):
    if 'yaml' not in name:
        name = name + '.yaml'
    path = os.path.join(CONFIG_DIR, folder, name)
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# TODO: clean this up more
def condition_to_sql(values, on='domain', allow_like=False):
    if not values:
        statement = "False"
    elif allow_like:
        statement = f'{on } like "%' + f'%" or {on} like "%'.join(values) + '%"'
    else:
        statement = f'{on } is "' + f'" or {on} is "'.join(values) + '"'
    return statement

def strip_excess_whitespace(x):
    x = re.sub('\n', ' ', x)
    x = re.sub('\s+', ' ', x)
    return x.lstrip('<p>').rstrip('</p>').strip()
