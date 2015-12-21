import requests
import jwt
from flask import\
    current_app
from functools import\
    wraps
from flask import\
    request
from src.utils import\
    get_config


def auth_error(message='Authentication Error'):
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
        if not auth:
            return auth_error(message='Expected authentication token!')

        res = validate_auth_token(auth=auth)
        if 'error' in res:
            return auth_error(message=res.error)

        return f(*args, **kwargs)
    return decorated


def limit(requests=100, window=30, by='ip', group=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if by is 'ip':
                identification = request.remote_addr or 'test'
            else:
                identification = by

            endpoint = group or request.endpoint

            key = ':'.join(['rl', endpoint, identification])

            try:
                remaining = requests - int(current_app.redis.get(key))
            except (ValueError, TypeError):
                remaining = requests
                current_app.redis.set(key, 0)

            ttl = current_app.redis.ttl(key)
            if ttl == -1:
                current_app.redis.expire(key, window)

            if remaining > 0:
                current_app.redis.incr(key, 1)
                return f(*args, **kwargs)
            else:
                return {'error': 'Too Many Requests', 'code': 429}
        return decorated
    return decorator
