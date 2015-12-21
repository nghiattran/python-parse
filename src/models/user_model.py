import json
from src.models.authentication_model import \
    generate_auth_token
from src.models import BaseModel
from src.utils import \
    send_activation_email,\
    random_string, \
    send_reset_password_email

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
            if status is not 200:
                return {'code': status, 'error': msg}
        return res

    def user_reset_password(self, where):
        where.pop('objectId', 0)
        params = {
            'where':json.dumps(where),
            'keys':'name,email,username'
        }

        user = self.get(
            collection='users',
            params=params)

        if 'error' in user:
            return user

        payload = {
            'objectId':user['results'][0]['objectId'],
            'password': random_string(15)
        }

        res = self.put(
            collection='users',
            object_id=payload['objectId'],
            payload=payload,
            master_key=True)

        if 'error' not in res:
            status, msg = send_reset_password_email(
                email=user['results'][0]['email'],
                username=user['results'][0]['username'],
                password=payload['password']
            )

            if status is not 200:
                return {'code': status, 'error': msg}
            res['email'] = {
                'status': status,
                'message': msg
            }
        return res
