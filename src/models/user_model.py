from src.models.authentication_model import \
    generate_auth_token
from src.models import BaseModel
from src.utils import send_activation_email

class UserModel(BaseModel):
    _parse_class_name = '_User'
    def user_login(self, params):
        res = self.login(params = params)
        if 'error' not in res:
            res['token'] = generate_auth_token(res);
        return res

    def user_signup(self, payload):
        res = self.signup(payload = payload)
        if 'error' not in res:
            res['token'] = generate_auth_token(res);
            status, msg = send_activation_email(email=payload['email'], objectId=res['objectId'])
        return res
