__author__ = 'nghia'

from app.models.TestModel import TestModel

from app.models.UserModel import UserModel
from app.forms.UserForm import UserForm

from flask_restful import Resource, Api

class BaseController(Resource):
    pass

class BaseTestController(BaseController):
    model = TestModel()

class BaseUserController(BaseController):
    model = UserModel()
    form = UserForm

