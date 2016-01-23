# @name <%= app_name %>
# @description
# Create connection between controllers and forms

from src.models.user_model import\
    UserModel
from src.forms.user_form import\
    UserGetForm,\
    UserPutForm, \
    UserSignupForm,\
    UserLoginForm,\
    UserResetPasswordForm,\
    AuthDataForm

from flask_restful import Resource, Api

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
