__author__ = 'nghia'
from flask import request
import json
from app.controllers import BaseUserController
import requests
from app.models.authentication_model import requires_auth

class UsersController(BaseUserController):

    @requires_auth
    def post(self):

        payload = {
            'username': request.args['username'],
            'password': request.args['password']
        }
        res = self.model.post(collection = 'users', payload = payload)
        return res

    @requires_auth
    def get(self):

        where = self.model.mapping_entry('_User')
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


    def put(self, objectId):
        where = {
            'objectId': objectId
        }

        params = {
            'where': json.dumps(where)
        }
        res = self.model.user_update(objectId=objectId)
        return res

    # def get(self, objectId):
    #     where = {
    #         'objectId': objectId
    #     }
    #     params = {
    #         'where': json.dumps(where)
    #     }
    #     res = self.model.get(collection = 'users', params = params)
    #     return res

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