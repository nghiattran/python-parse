__author__ = 'nghia'

from app.models.TestModel import TestModel
from app.models.UserModel import UserModel
from app.forms.UserForm import UserForm
from app.utils import validate_auth_token

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

