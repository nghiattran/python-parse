
import json
from src.controllers import\
    BaseUserController
from src.models.authentication_model import\
    requires_auth,\
    limit

_parse_class_name = BaseUserController.model._parse_class_name


class UsersController(BaseUserController):
    # Require authentication token
    @requires_auth
    # Limit number of requests per IP
    @limit(requests=100, window=30, by='ip', group=None)
    # Limit number of requests per second
    @limit(requests=30, window=1, by='parse', group='parse')
    def get(self):
        form = self.get_form()
        params = form.data

        res = self.model.get(
            collection='users',
            params=params)
        return res


class UserController(BaseUserController):
    @requires_auth
    @limit(requests=100, window=30, by='ip', group=None)
    @limit(requests=30, window=1, by='parse', group='parse')
    def get(self, object_id):
        where = {
            'objectId': object_id
        }
        params = {
            'where': json.dumps(where)
        }
        res = self.model.get(
            collection='users',
            params=params)
        return res

    @requires_auth
    @limit(requests=100, window=30, by='ip', group=None)
    @limit(requests=30, window=1, by='parse', group='parse')
    def put(self, object_id):
        form = self.put_form()
        payload = form.data

        res = self.model.put(
            collection='users',
            object_id=object_id,
            payload=payload,
            master_key=True)
        return res

    @requires_auth
    @limit(requests=100, window=30, by='ip', group=None)
    @limit(requests=30, window=1, by='parse', group='parse')
    def delete(self, object_id):
        res = self.model.delete(
            collection='users',
            object_id=object_id,
            master_key=True
        )
        return res


class SignupController(BaseUserController):
    @limit(requests=100, window=30, by='ip', group=None)
    @limit(requests=30, window=1, by='parse', group='parse')
    def post(self):
        form = self.signup_form()
        payload = form.data

        res = self.model.user_signup(
            payload=payload
        )
        return res


class LoginController(BaseUserController):
    @limit(requests=100, window=30, by='ip', group=None)
    @limit(requests=30, window=1, by='parse', group='parse')
    def get(self):
        form = self.login_form()
        params = form.data

        res = self.model.user_login(
            params= params
        )
        return res


class ResetpasswordController(BaseUserController):
    @limit(requests=100, window=30, by='ip', group=None)
    @limit(requests=30, window=1, by='parse', group='parse')
    def post(self):
        form = self.reset_password_form()
        payload = form.data

        res = self.model.password_reset(
            payload=payload
        )
        return res

class AuthController(BaseUserController):
    @limit(requests=100, window=30, by='ip', group=None)
    @limit(requests=30, window=1, by='parse', group='parse')
    def post(self):
        form = self.auth_form()
        payload = form.data

        res = self.model.user_signup(
            payload=payload
        )

        return res

class UserActivationController(BaseUserController):
    @limit(requests=100, window=30, by='ip', group=None)
    @limit(requests=30, window=1, by='parse', group='parse')
    def get(self, object_id):
        payload = {
            'emailVerified': True
        }

        res = self.model.put(
            collection='users',
            object_id=object_id,
            payload=payload,
            master_key=True)
        return res
