# @name testApp
# @description
# Create connection between controllers and forms

from flask_restful import Resource, Api
from src.models.user_model import\
    UserModel
from src.forms.user_form import\
    UserGetForm,\
    UserPutForm, \
    UserSignupForm,\
    UserLoginForm,\
    UserResetPasswordForm,\
    AuthDataForm
# MARKED: DO NOT REMOVE THIS LINE, generator-python-parse needs it to work
# properply

class BaseController(Resource):
    pass

class BaseUserController(BaseController):
    model = UserModel()
    get_form = UserGetForm
    put_form = UserPutForm
    signup_form = UserSignupForm
    login_form = UserLoginForm
    auth_form = AuthDataForm
    reset_password_form = UserResetPasswordForm
