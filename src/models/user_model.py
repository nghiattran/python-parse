__author__ = 'nghia'
from src.models.authentication_model import \
    generate_auth_token
from src.models import BaseModel
from flask import \
    request


class UserModel(BaseModel):
    _parse_class_name = '_User'
    def user_login(self, params):
        res = self.login(params = params)
        res['token'] = generate_auth_token(res);
        return res

    def user_signup(self, payload):
        res = self.signup(payload = payload)
        res['token'] = generate_auth_token(res);
        return res

    def user_resetpassword(self, payload):
        res = self.password_reset(payload = payload)
        return res

    def user_update(self, objectId):
        payload = self.mapping_entry(class_name=self._parse_class_name)
        return payload