__author__ = 'nghia'

from src.models.test_model import TestModel
from src.models.user_model import UserModel
from src.forms.UserForm import UserForm
from src.models.authentication_model import validate_auth_token

from flask_restful import Resource, Api

class BaseController(Resource):
    def validate_authetication(self, token):
        res = validate_auth_token(token)
        if 'error' in res:
            return False
        return True

class BaseTestController(BaseController):
    model = TestModel()

class BaseUserController(BaseController):
    model = UserModel()
    form = UserForm

