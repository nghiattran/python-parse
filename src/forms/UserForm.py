__author__ = 'nghia'

from wtforms import\
    Form,\
    validators,\
    StringField,\
    IntegerField,\
    HiddenField,\
    BooleanField
from src.forms import \
    BaseGetForm,\
    BasePostForm

class UserGetForm(BaseGetForm):
    pass

class UserSignupForm(BasePostForm):
    username = StringField()
    password = HiddenField()

class UserLoginForm(BaseGetForm):
    username = StringField()
    password = HiddenField()

class UserResetPasswordForm(BasePostForm):
    email = StringField()
