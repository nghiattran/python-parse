__author__ = 'nghia'
import jwt
import json

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

def generate_auth_token(payload):
    return jwt.encode(payload=payload, key=get_config(key='JWT_KEY'))

def validate_auth_token(token):
    try:
        return jwt.decode(jwt=token, key=get_config(key='JWT_KEY'))
    except jwt.ExpiredSignature:
        return {'error': 'Token is expired'}
    except jwt.DecodeError:
        return {'error': 'Token signature is invalid'}
    except Exception:
        return {'error': 'Problem parsing token'}