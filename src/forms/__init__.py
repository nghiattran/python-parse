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

PARSE_MAX_LIMIT = 1000

class BaseAPIForm(Form):
    objectId = HiddenField()
    # where to parse the data from request object (json, args, _headers, form)
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
                # throw error for bad JSON:
                if self._data_location == 'json':
                    raise ValidationError("Invalid JSON1")
                else:
                    raise e

            if self._data_location == 'json' and type(data) is not dict:
                raise ValidationError('Invalid JSON2')

            formdata = MultiDict(data)

        super(BaseAPIForm, self).__init__(
            formdata=formdata,
            obj=obj,
            prefix=prefix)
        pass

class JSONField(StringField):
    def pre_validate(self, form):
        if self.data and type(self.data) is not dict:
            try:
                self.data = json.loads(self.data)
            except:
                raise ValidationError("Invalid JSON Field")

        return super(JSONField, self).pre_validate(form)

class BaseGetForm(BaseAPIForm):
    _data_location = 'args'

    where = JSONField(default={})
    count = IntegerField(default=0)
    order = StringField([validators.optional()])
    skip = IntegerField(default=0)
    limit = IntegerField(default=PARSE_MAX_LIMIT)
    include = StringField(default=None)
    keys = StringField([validators.optional()])

class BasePostForm(BaseAPIForm):
    _data_location = 'json'

class BasePutForm(BaseAPIForm):
    _data_location = 'json'

class BaseDeleteForm(BaseAPIForm):
    _data_location = 'args'