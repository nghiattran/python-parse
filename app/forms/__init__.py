from wtforms import (Form, validators, StringField, IntegerField,
                     HiddenField, BooleanField)
from werkzeug.datastructures import MultiDict
from werkzeug.exceptions import BadRequest
from wtforms.validators import ValidationError
from flask import request, json

class BaseAPIForm(Form):
    objectId = HiddenField()
    # where to parse the data from request object (json, args, _headers, form)
    _data_location = 'json'
    _formdata = ''
    error_message = 'Unknown Error'

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        # if formdata is None and self._data_location:
        #     # get form data from request:
        #     try:
        #         data = getattr(request, self._data_location, MultiDict())
        #     except BadRequest, e:
        #         # throw error for bad JSON:
        #         if self._data_location == 'json':
        #             raise ValidationError("Invalid JSON1")
        #         else:
        #             # print 'not sure what to do....'
        #             raise e
        #
        #     # json data must be a valid dict, not unicode string:
        #     if self._data_location == 'json' and type(data) is not dict:
        #         raise ValidationError('Invalid JSON2')
        #
        #     # strip out empty value:
        #     formdata = MultiDict(data)
        #     self._formdata = formdata
        #
        # super(BaseAPIForm, self).__init__(formdata=formdata, obj=obj,
        #                                   prefix=prefix)
        pass
class BaseUserForm(BaseAPIForm):
    pass