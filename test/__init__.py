import json
import string
import random
import unittest
import requests
import urllib
from app import\
    app
from src.utils import\
    get_config
from click.testing import\
    CliRunner
from flask.testing import\
    FlaskClient
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

class TestClient(FlaskClient):
    def open(self, *args, **kw):
        """
        Overriding open to add in Auth token header
        """
        headers = [
            ("Authentication", get_config(key="TEST_TOKEN"))
        ]

        # set default header to be json
        content_type = "application/json"
        if 'data' in kw and 'file' in kw['data'] and 'profile' not in \
                kw['data']:
            content_type = "multipart/form-data"
        headers.append(("Content-Type", content_type))

        if kw.get('headers'):
            kw['headers'].append(headers)
        else:
            kw['headers'] = headers

        return super(TestClient, self).open(*args, **kw)

class BaseTestCase(unittest.TestCase):
    cli = CliRunner()
    config = app.config

    def setUp(self):
        self.app = TestClient(app, app.response_class)
        self.prefix_url = get_config(key="TEST_API_URL") + "/"

    def generate_header(self, master_key = None):
        header = {
            "Authentication": get_config(key="TEST_TOKEN"),
            "Content-Type": "application/json"
        }

        return header


    def generate_url(self, url):
        url = "{}/{}".format(
            get_config(key="TEST_API_URL"),
            url
        )
        return url


    def get(self, url, params = None):
        url = self.generate_url(url = url)
        headers= self.generate_header()
        if params:
            params = urllib.urlencode(params)
        
        res = requests.get(url=url,
                               headers=headers,
                               params=params)
        return res.json()

    def get_data(self, url, params=None):
        url = self.prefix_url + url
        res = self.app.get(url, query_string=params)
        return json.loads(res.data)

    def post_data(self, url, data=None):
        if type(data) is dict:
            data = json.dumps(data)
        url = self.prefix_url + url
        res = self.app.post(url, data=data)

        return json.loads(res.data)

    def put_data(self, url, data):
        if type(data) is dict:
            data = json.dumps(data)
        url = self.prefix_url + url
        res = self.app.put(url, data=data)

        return json.loads(res.data)

    def delete_data(self, url):
        url = self.prefix_url + url
        res = self.app.delete(url)

        return json.loads(res.data)

    def random_string(self, length = 20, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(length))