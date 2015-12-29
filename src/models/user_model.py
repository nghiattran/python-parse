import json
from src.models.authentication_model import \
    generate_auth_token
from src.models import BaseModel
from src.utils import random_string
from src.models.email_model import send_activation_email, send_reset_password_email

class UserModel(BaseModel):
    _parse_class_name = '_User'

    def user_update(self, payload, object_id):
        # Params for checking user's credentials and payload for updating
        params = payload.copy()
        remove = ('username','password','old_password','re_old_password')
        for object in remove:
            payload.pop(object, None)
        if 'old_password' in params:
            payload['password'] = params['password']
            params['password'] = params['old_password']

        # Login to check user's credentials first
        res = self.login(params = params)
        if 'error' in res:
            return res

        # Perform updating
        res = self.put(
            collection='users',
            object_id=object_id,
            payload=payload,
            master_key=True)
        return res

    def user_login(self, params):
        res = self.login(params = params)

        # Generate user's token
        if 'error' not in res:
            res['token'] = generate_auth_token(res);
        return res

    def user_signup(self, payload):
        res = self.signup(payload = payload)

        # Generate user's token
        if 'error' not in res:
            res['token'] = generate_auth_token(res);
            status, msg = send_activation_email(email=payload['email'], objectId=res['objectId'])
            if status is not 200:
                return {'code': status, 'error': msg}
        return res

    def user_reset_password(self, where):
        # Get user's infomation for sending email
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
        elif len(user['results']) != 1:
            return {
                'error':404,
                'message': 'Invalid email'
            }

        # Reset user's password
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
            # Sending notification email
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
