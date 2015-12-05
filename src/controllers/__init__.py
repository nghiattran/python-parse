
from src.models.user_model import\
    UserModel
from src.forms.user_form import\
    UserGetForm,\
    UserPutForm, \
    UserSignupForm,\
    UserLoginForm,\
    UserResetPasswordForm
from src.models.authentication_model import\
    validate_auth_token

from flask_restful import Resource, Api

class BaseController(Resource):
    def validate_authetication(self, token):
        res = validate_auth_token(token)
        if 'error' in res:
            return False
        return True

class BaseUserController(BaseController):
    model = UserModel()
    get_form = UserGetForm
    put_form = UserPutForm
    signup_form = UserSignupForm
    login_form = UserLoginForm
    reset_password_form = UserResetPasswordForm
