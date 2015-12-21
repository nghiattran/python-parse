from wtforms import\
    Form,\
    validators,\
    StringField,\
    IntegerField,\
    HiddenField,\
    BooleanField,\
    PasswordField
from src.forms import \
    BaseGetForm,\
    BasePostForm,\
    BasePutForm,\
    JSONField

class UserGetForm(BaseGetForm):
    username = StringField()
    password = HiddenField()
    phone = StringField()
    email = StringField()

class UserPutForm(BasePutForm):
    username = StringField('Username', [
        validators.DataRequired(message="username required")
    ])
    password = PasswordField('Password', [validators.DataRequired()])

    old_password = PasswordField('Old Password', [
        validators.EqualTo('re_old_password')])
    re_old_password = PasswordField('Confirm', [])
    phone = StringField()
    email = StringField()

class UserSignupForm(BasePostForm):
    username = StringField()
    password = HiddenField()
    email = StringField()

class UserLoginForm(BaseGetForm):
    username = StringField()
    password = HiddenField()

class UserResetPasswordForm(BasePostForm):
    email = StringField()

class AuthDataForm(BasePostForm):
    authData = JSONField()
