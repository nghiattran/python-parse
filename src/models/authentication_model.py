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


def check_request_limit(requests=100, window=30, by='ip', group=None):
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
    else:
        raise IOError({'error': 'Too Many Requests', 'code': 429})


# limit_wrapper is a decorator to controller number of requests are made to server to avoid attacks
# and limit database cost. By default, it limit 100 requests/30s interval/1 IP address and 30
# request/second/all IP addresses
def check_all_request_limit(wrapped):
    def wrapper(*args, **kwargs):
        try:
            request_limits = get_config(key='REQUEST_LIMITS')
            per_ip_limit = request_limits['PER_IP_LIMIT']
            parse_limit = request_limits['PARSE_LIMIT']

            # Limit number of requests per IP adress
            check_request_limit(
                requests=per_ip_limit['NUM_REQUESTS'],
                window=per_ip_limit['INTERVAL'],
                by='ip',
                group=None
            )

            # Limit number of requests per second
            check_request_limit(
                requests=parse_limit['NUM_REQUESTS'],
                window=parse_limit['INTERVAL'],
                by='parse',
                group='parse'
            )
        except IOError as err:
            return err.message

        return wrapped(*args, **kwargs)
    return wrapper
