import os
from pathlib import Path

import yaml


CONFIG_DIR = os.path.join(Path(__file__).parents[2], 'config')


def read_config(folder, name):
    if 'yaml' not in name:
        name = name + '.yaml'
    path = os.path.join(CONFIG_DIR, folder, name)
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
    return config
