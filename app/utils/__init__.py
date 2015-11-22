__author__ = 'nghia'
import json
from flask import\
    request
CONFIG = None
CONFIG_SCHEMA = None

def get_config(key = None):
    global CONFIG
    if CONFIG is None:
        config_file = 'config/dev.json'
        with open(config_file) as data_file:
            CONFIG = json.load(data_file)

    if CONFIG and key in CONFIG:
        return CONFIG[key]

    return CONFIG

def get_schema(key = None):
    global CONFIG_SCHEMA
    if CONFIG_SCHEMA is None:
        config_file = 'config/schema.json'
        with open(config_file) as data_file:
            CONFIG_SCHEMA = json.load(data_file)

    if CONFIG_SCHEMA and key in CONFIG_SCHEMA:
        return CONFIG_SCHEMA[key]

    return CONFIG_SCHEMA

