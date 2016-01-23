# @name <%= app_name %>
# @description
# UserControler handles everything related to users' information from
# registration, verification, authenciation, ....

import json
from src.controllers import\
    BaseUserController
from src.models.authentication_model import\
    requires_auth,\
    check_all_request_limit

_parse_class_name = BaseUserController.model._parse_class_name


class UsersController(BaseUserController):
    # Require authentication token
    @requires_auth
    @check_all_request_limit
    def get(self):
        form = self.get_form()
        if form.validate():
            params = form.filter_data()

            res = self.model.get(
                collection='users',
                params=params)

            res['params'] = params
            return res

        return {'error': 'Unvalid inputs', 'code': 400}


class UserController(BaseUserController):
    @requires_auth
    @check_all_request_limit
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
    @check_all_request_limit
    def put(self, object_id):
        form = self.put_form()
        if form.validate():
            payload = form.filter_data()

            res = self.model.user_update(
                payload=payload,
                object_id=object_id)
            return res

        return {'error': 'Unvalid inputs', 'code': 400}

    @requires_auth
    @check_all_request_limit
    def delete(self, object_id):
        res = self.model.delete(
            collection='users',
            object_id=object_id,
            master_key=True
        )
        return res


class SignupController(BaseUserController):
    @check_all_request_limit
    def post(self):
        form = self.signup_form()
        if form.validate():
            payload = form.filter_data()

            res = self.model.user_signup(
                payload=payload
            )
            return res

        return {'error': 'Unvalid inputs', 'code': 400}


class LoginController(BaseUserController):
    @check_all_request_limit
    def get(self):
        form = self.login_form()
        if form.validate():
            params = form.filter_data()

            res = self.model.user_login(
                params=params
            )
            return res
        return {'error': 'Unvalid inputs', 'code': 400}


class ResetpasswordController(BaseUserController):
    @check_all_request_limit
    def post(self):
        form = self.reset_password_form()
        if form.validate():
            where = form.filter_data()

            res = self.model.user_reset_password(
                where=where
            )
            return res
        return {'error': 'Unvalid inputs', 'code': 400}


class AuthController(BaseUserController):
    @check_all_request_limit
    def post(self):
        form = self.auth_form()
        if form.validate():
            payload = form.filter_data()
            res = self.model.user_signup(
                payload=payload
            )

            return res
        return {'error': 'Unvalid inputs', 'code': 400}


class UserActivationController(BaseUserController):
    @check_all_request_limit
    def get(self, object_id):
        payload = {
            'email_verified': True
        }

        res = self.model.put(
            collection='users',
            object_id=object_id,
            payload=payload,
            master_key=True)
        return res
