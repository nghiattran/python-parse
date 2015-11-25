__author__ = 'nghia'

import json
from test import BaseTestCase


class UserTestCase(BaseTestCase):
    # Test get
    def test_get_data_all(self):
        params = {
            'where': {}
        }
        res = self.get_data(url='users', params=params)

        assert 'results' in res
        assert len(res['results']) > 0
        
    def test_get_data_specific_entry(self):
        params = {
        }
        res = self.get_data(url='users', params=params)
        res = self.get_data(url='users/' + res['results'][0]['objectId'])

        assert 'results' in res
        assert len(res['results']) is 1

    def test_get_data_limit_one(self):
        params = {
            "limit": 1
        }
        res = self.get_data(url='users', params=params)

        assert 'results' in res
        assert len(res['results']) is 1
        
    def test_get_data_limit_ten(self):
        params = {
            "limit": 10
        }
        res = self.get_data(url='users', params=params)
        assert 'results' in res
        assert len(res['results']) is 10

    def test_get_data_count(self):
        params = {
            "count": 1
        }
        res = self.get_data(url='users', params=params)

        assert 'results' in res
        assert 'count' in res

    # Test login

    def test_login(self):

        pass

    # Test signup

    def test_signup(self):
        payload = {
            'username': self.random_string(length=20),
            'password': 'testing'
        }
        res = self.post_data(url='signup', data=payload)

        assert 'createdAt' in res
        assert 'token' in res