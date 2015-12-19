from wtforms import\
    Form,\
    validators,\
    StringField,\
    IntegerField,\
    HiddenField,\
    BooleanField
from src.forms import \
    BaseGetForm,\
    BasePostForm,\
    BasePutForm

class UserGetForm(BaseGetForm):
    username = StringField()
    password = HiddenField()
    phone = StringField()
    email = StringField()

class UserPutForm(BasePutForm):
    username = StringField()
    password = HiddenField()
    phone = StringField()

class UserSignupForm(BasePostForm):
    username = StringField()
    password = HiddenField()
    email = StringField()

class UserLoginForm(BaseGetForm):
    username = StringField()
    password = HiddenField()

class UserResetPasswordForm(BasePostForm):
    email = StringField()
