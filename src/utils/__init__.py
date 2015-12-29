import json
import os
import random
import string

CONFIG = None
CONFIG_SCHEMA= None


def get_config(
        config_env='API_CONFIG',
        key= None):
    global CONFIG
    if CONFIG is None:
        if config_env in os.environ:
            config_file = os.environ[config_env]
            with open(config_file) as data_file:
                CONFIG = json.load(data_file)
        else:
            config_file = 'config/dev.json'
            with open(config_file) as data_file:
                CONFIG = json.load(data_file)

    if CONFIG and key in CONFIG:
        return CONFIG[key]

    return CONFIG

def random_string(length = 20, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(length))