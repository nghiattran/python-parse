__author__ = 'nghia'

import json
import requests
from app.utils import get_config, generate_auth_token
import urllib
from requests.exceptions import ConnectionError

PARSE_MAX_LIMIT = 1000

class BaseModel(object):

    _parse_special_classes = ['apps', 'users', 'login', 'roles', 'files',
                              'events',
                              'push', 'installations', 'functions', 'jobs',
                              'requestPasswordReset', 'products',
                              'roles', 'batch', 'schemas']

    def generate_header(self):
        return {
            "X-Parse-Application-Id": get_config("PARSE_APP_ID"),
            "X-Parse-REST-API-Key": get_config("PARSE_REST_KEY"),
            "Content-Type": "application/json"
        }

    def generate_url(self, collection, objectId = None):
        base_url = get_config("PARSE_URL")

        if collection in self._parse_special_classes:
            url = "{}/{}".format(base_url, collection)
        else:
            url = "{}/classes/{}".format(base_url, collection)

        if objectId is not None:
            url = "{}/{}".format(url, objectId)

        return url

    def get(self, collection, params):
        url = self.generate_url(collection = collection)
        headers= self.generate_header()
        params = urllib.urlencode(params)

        try:
            res = requests.get(url=url, headers=headers,
                               params=params)
            return res.json()
        except ConnectionError as e:
            return {'error': "Cannot connect to database. "
                             "Please try again later."}
        except Exception as e:
            return {'error': e.message}

    def post(self, collection, payload):
        url = self.generate_url(collection = collection)
        headers= self.generate_header()
        # headers['X-Parse-Revocable-Session'] = 0

        try:
            res = requests.post(url=url, headers=headers,
                                   data=json.dumps(payload))
            return res.json()
        except ConnectionError as e:
            return {'error': "Cannot connect to database. "
                             "Please try again later."}
        except Exception as e:
            return {'error': e.message}

    def put(self, collection, objectId, payload):
        url = self.generate_url(collection = collection, objectId = objectId)
        headers= self.generate_header()

        try:
            payload = requests.put(url=url, headers=headers,
                                   payload=json.dumps(payload))
            return payload.json()
        except ConnectionError as e:
            return {'error': "Cannot connect to database. "
                             "Please try again later."}
        except Exception as e:
            return {'error': e.message}

    def delete(self, collection, objectId):
        url = self.generate_url(collection = collection, objectId = objectId)
        headers= self.generate_header()

        try:
            res = requests.delete(url=url, headers=headers)
            return res.json()
        except ConnectionError as e:
            return {'error': "Cannot connect to database. "
                             "Please try again later."}
        except Exception as e:
            return {'error': e.message}

    def login(self, params):
        res = self.get(collection = "login", params=params)
        return res

    def signup(self, payload):
        res = self.post(collection = "users", payload=payload)
        return res

    def password_reset(self, payload):
        res = self.post(collection = "requestPasswordReset", payload=payload)
        return res
