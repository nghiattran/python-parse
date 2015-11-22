__author__ = 'nghia'
from functools import\
    wraps
from flask import\
    request
import requests
import jwt

from app.utils import get_config

def auth_error(message="Authentication Error"):
    res = {'error': message}
    res['code'] = requests.codes.forbidden
    return res

def generate_auth_token(payload):
    return jwt.encode(payload=payload, key=get_config(key='JWT_KEY'))

def validate_auth_token(auth):
    try:
        return jwt.decode(jwt=auth, key=get_config(key='JWT_KEY'))
    except jwt.ExpiredSignature:
        return {'error': 'Token is expired'}
    except jwt.DecodeError:
        return {'error': 'Token signature is invalid'}
    except Exception:
        return {'error': 'Problem parsing token'}

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authentication', None)
        print auth
        if not auth:
            return auth_error(message="Expected authentication token!")

        res = validate_auth_token(auth=auth)
        if 'error' in res:
            return auth_error(message=res.error)

        return f(*args, **kwargs)
    return decorated



