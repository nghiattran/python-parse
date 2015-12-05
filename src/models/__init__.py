import json
import requests
import urllib
from src.utils import\
    get_config
from requests.exceptions import\
    ConnectionError

PARSE_MAX_LIMIT = 1000

class BaseModel(object):
    _parse_class_name = None
    _parse_special_classes = ['apps', 'users', 'login', 'roles',
                              'files', 'events', 'push',
                              'installations', 'functions', 'jobs',
                              'requestPasswordReset', 'products',
                              'roles', 'batch', 'schemas']

    def generate_header(self, master_key = None):
        header = {
            "X-Parse-Application-Id": get_config(key="PARSE_APP_ID"),
            "X-Parse-REST-API-Key": get_config(key="PARSE_REST_KEY"),
            "Content-Type": "application/json"
        }
        if master_key:
            header['X-Parse-Master-Key']= get_config(key="PARSE_MASTER_KEY")

        return header

    def generate_url(self, collection, object_id = None):
        base_url = get_config(key="PARSE_URL")

        if collection in self._parse_special_classes:
            url = "{}/{}".format(base_url, collection)
        else:
            url = "{}/classes/{}".format(base_url, collection)

        if object_id is not None:
            url = "{}/{}".format(url, object_id)

        return url

    def get(self, collection, params, master_key=None):
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

    def post(self, collection, payload, master_key=None):
        url = self.generate_url(collection = collection)
        headers= self.generate_header()

        try:
            res = requests.post(url=url, headers=headers,
                                   data=json.dumps(payload))
            return res.json()
        except ConnectionError as e:
            return {'error': "Cannot connect to database. "
                             "Please try again later."}
        except Exception as e:
            return {'error': e.message}

    def put(self, collection, object_id, payload, master_key=None):
        url = self.generate_url(collection = collection, object_id = object_id)
        headers= self.generate_header(master_key=master_key)

        try:
            payload = requests.put(url=url, headers=headers,
                                   data=json.dumps(payload))
            return payload.json()
        except ConnectionError as e:
            return {'error': "Cannot connect to database. "
                             "Please try again later."}
        except Exception as e:
            return {'error': e.message}

    def delete(self, collection, object_id, master_key = None):
        url = self.generate_url(collection = collection, object_id = object_id)
        headers= self.generate_header(master_key=master_key)

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
