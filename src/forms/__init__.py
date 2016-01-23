# @name <%= app_name %>
# @description
# Utility functions for all Forms.

import json
from wtforms import\
    Form,\
    HiddenField,\
    IntegerField,\
    validators,\
    BooleanField,\
    StringField
from werkzeug.datastructures import\
    MultiDict
from werkzeug.exceptions import\
    BadRequest
from wtforms.validators import\
    ValidationError
from flask import\
    request

# Maximum number of objects can be returned set by Parse.com
PARSE_MAX_LIMIT = 1000

# BaseAPIForm is for parsing data from request object, getting rid of
# unexpected data, and validate data
class BaseAPIForm(Form):
    objectId = HiddenField()
    _data_location = 'json'
    _formdata = ''

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        if formdata is None and self._data_location:
            try:
                data = getattr(
                    request,
                    self._data_location,
                    MultiDict()
                )
            except BadRequest, e:
                if self._data_location == 'json':
                    raise ValidationError("Invalid JSON1")
                else:
                    raise e

            if self._data_location == 'json' and type(data) is not dict:
                raise ValidationError('Invalid JSON2')

            self._formdata = MultiDict(data)

        super(BaseAPIForm, self).__init__(
            formdata=self._formdata,
            obj=obj,
            prefix=prefix)


    def filter_data(self):
        payload = {}
        for key in self._formdata.viewkeys() & self.data.viewkeys():
            payload[key] = self.data[key]

        return payload


    def validate(self):
        validate_result = super(BaseAPIForm, self).validate()
        if not validate_result:
            for k, v in self.errors.iteritems():
                self.error_message = v[0]
                break
            return False
        return validate_result


class JSONField(StringField):
    def pre_validate(self, form):
        if self.data and type(self.data) is not dict:
            try:
                self.data = json.loads(self.data)
            except:
                raise ValidationError("Invalid JSON Field")
        return super(JSONField, self).pre_validate(form)


# 4 BaseForm classes describe where to look for information in request header.
class BaseGetForm(BaseAPIForm):
    _data_location = 'args'

    where = JSONField(default={})
    count = IntegerField(default=0)
    order = StringField([validators.optional()])
    skip = IntegerField(default=0)
    limit = IntegerField(default=PARSE_MAX_LIMIT)
    include = StringField(default=None)
    keys = StringField([validators.required()])


class BasePostForm(BaseAPIForm):
    _data_location = 'json'


class BasePutForm(BaseAPIForm):
    _data_location = 'json'


class BaseDeleteForm(BaseAPIForm):
    _data_location = 'args'
