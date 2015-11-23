__author__ = 'nghia'

from wtforms import (Form, validators, StringField, IntegerField,
                     HiddenField, BooleanField)
from src.forms import BaseUserForm

class UserForm(BaseUserForm):
    _data_location = 'json'
    username = StringField()
    password = HiddenField()
