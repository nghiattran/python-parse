__author__ = 'nghia'
from flask import request
import json
from app.controllers import BaseUserController
import urllib

class UsersController(BaseUserController):

    def post(self):
        payload = {
            'username': request.args['username'],
            'password': request.args['password']
        #     add more data for user here
        }
        res = self.model.post(collection = 'users', payload = payload)
        return res

    def get(self):
        where = {
            'username': 'one'
        }
        params = {
            'where': json.dumps(where)
        }
        res = self.model.get(collection = 'users', params = params)
        return res

class UserController(BaseUserController):
    def get(self, objectId):
        where = {
            'objectId': objectId
        }
        params = {
            'where': json.dumps(where)
        }
        res = self.model.get(collection = 'users', params = params)
        return res

class SignupController(BaseUserController):
    def post(self):
        payload = {
            'username': request.args['username'],
            'password': request.args['password']
        }
        res = self.model.user_signup(payload = payload)
        return res

class LoginController(BaseUserController):
    def get(self):
        params = {
            'username': request.args['username'],
            'password': request.args['password']
        }
        res = self.model.user_login(params = params)
        return res

class ResetpasswordController(BaseUserController):
    def post(self):
        payload = {
            'email': request.args['email']
        }
        res = self.model.password_reset(payload = payload)
        return res