import json
from test import BaseTestCase


class UserTestCase(BaseTestCase):
    # Test signup

    def test_signup(self):
        payload = {
            'username': self.random_string(length=20),
            'password': 'testing'
        }
        res = self.post_data(url='signup', data=payload)

        assert 'createdAt' in res
        assert 'token' in res

    def test_signup_with_existing_username(self):
        params = {
            'keys': 'username'
        }
        res = self.get_data(url='users', params=params)

        payload = {
            'username': res['results'][0]['username'],
            'password': 'testing'
        }
        res = self.post_data(url='signup', data=payload)

        assert 'error' in res

    # Test get
    def test_get_data_all(self):
        res = self.get_data(url='users', params={})

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
            'limit': 1
        }
        res = self.get_data(url='users', params=params)

        assert 'results' in res
        assert len(res['results']) is 1

    def test_get_data_limit_ten(self):
        params = {
            'limit': 1
        }
        res = self.get_data(url='users', params=params)
        assert 'results' in res
        assert len(res['results']) is 1

    def test_get_data_count(self):
        params = {
            'count': 1
        }
        res = self.get_data(url='users', params=params)

        assert 'results' in res
        assert 'count' in res

    # Test login

    def test_login(self):
        params = {
            'keys': 'phone,username'
        }
        res = self.get_data(url='users', params=params)

        params = {
            'username': res['results'][0]['username'],
            'password': 'testing'
        }
        res = self.get_data(url='login', params=params)

        assert 'objectId' in res
        assert 'token' in res

    # Test put

    def test_put(self):
        params = {
            'keys': 'phone,username'
        }
        res = self.get_data(url='users', params=params)
        url = 'users/' + res['results'][0]['objectId']
        payload = {
            'username': res['results'][0]['username'],
            'password': 'testing',
            'phone': 'phone has changed'
        }
        res = self.put_data(url=url, data=payload)

        assert 'updatedAt' in res
        assert res['phone'] in 'phone has changed'

    # Test delete

    def test_delete(self):
        payload = {
            'username': self.random_string(length=20),
            'password': 'testing'
        }
        res = self.post_data(url='signup', data=payload)

        url = 'users/' + res['objectId']
        res = self.delete_data(url=url)

        assert 'error' not in res
