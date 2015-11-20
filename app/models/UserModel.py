__author__ = 'nghia'
from app.utils import generate_auth_token

from app.models import BaseModel

class UserModel(BaseModel):
    def user_login(self, params):
        res = self.login(params = params)
        token = generate_auth_token(res);
        if 'error' not in res:
            res['token'] = token

        return res

    def user_signup(self, payload):
        res = self.signup(payload = payload)
        token = generate_auth_token(res);
        if 'error' not in res:
            res['token'] = token

        return res

    def user_resetpassword(self, payload):
        res = self.password_reset(payload = payload)

        return res