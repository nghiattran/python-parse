#Work on prgress

[![Build Status](https://travis-ci.org/nghiattran/python-parse.svg?branch=master)](https://travis-ci.org/nghiattran/python-parse)&nbsp;&nbsp;[![Coverage Status](https://coveralls.io/repos/nghiattran/python-parse/badge.svg?branch=master&service=github)](https://coveralls.io/github/nghiattran/python-parse?branch=master)

#Python-parse
    Python API template for backend system using parse.com as database.

[![image](python-parse.png)](https://github.com/nghiattran/python-parse)

[Roadmap](https://github.com/nghiattran/python-parse#road-map)&nbsp;&nbsp;&nbsp;[Getting Started](https://github.com/nghiattran/python-parse#getting-started)&nbsp;&nbsp;&nbsp;[API architecture](https://github.com/nghiattran/python-parse/tree/master#api-architecture)

#Road map

List of planning features:

- [x] Limit request per ip
- [x] Limit request per interval
- [ ] Email automation
- [ ] Update documentation

# Getting started

###Installation
    
    # install all dependencies
    bin/install
 
###Start
    
    # start redis
    bin/start_redis
    #start api in port 8000
    bin/install
    
###Testing
    
    # run normal tests
    bin/test
    # or run a specific test file
    bin/test path/to/file

    # not available yet
    # run mock tests
    bin/mock
    # or run a specific mock test file
    bin/mock path/to/file

    # run coverage
    bin/cover

    # clean up
    bin/clean

#API architecture

    bin
        \- install                          # install all dependencies
        \- start_redis                      # start redis
        \- start                            # start service   
        \- test                             # run live tests
        \- mock                             # run mock tests (in future)
        \- cover                            # run coverage
        \- clean                            # clean coverage
    app.py                                  # create app and set routes
    src
        \- controllers                      
            \- __init__                     # set up controllers and their associates
            \- user_controller.py           # controller to handle user data
        \- forms
            \- __init__                     # set up base form
            \- user_form.py                 # form to handle user data
        \- models
            \- __init__                     # set up base model
            \- user_model.py                # model to handle user data
        \- utils
            \- __init__                     # utility functions
    test
        \- live                             # branch for live tests
            \- integration                  # branch for integration test
                \- test_user.py             # tests for user_controller

#How to use

###Open an API endpoint

Example: open `/users` endpoint.

* Create `<endpoint_name>_form.py` in this case `user_form.py`:
This file plays as a filter for incomming data.

``` python
from wtforms import\
    StringField,\
    HiddenField,
from src.forms import \
    BaseGetForm,

class UserGetForm(BaseGetForm):
    username = StringField()
    password = HiddenField()
```

`BaseGetForm` is for filtering `limit`, `count`, `keys`, . . .
All accessible data need to be placed in`UserGetForm` or will be ignored. As in this case only `username` and `password` are included.

* Create `<endpoint_name>_model.py` in this case `user_model.py`:
This file is adding headers and sending requests to Parse.com.

``` python
from src.models.authentication_model import \
    generate_auth_token
from src.models import BaseModel

class UserModel(BaseModel):
    _parse_class_name = '_User'

    def user_signup(self, payload):
        res = self.signup(payload = payload)
        if 'error' not in res:
            res['token'] = generate_auth_token(res);
        return res
```

`_parse_class_name` specifies which class or table you want to access in database

`BaseModel` is for adding headers.

As you see, `user_signup` receives `payload` containing user's credentials and send request to Parse by calling `res = self.signup(payload = payload)`

If the request success, a session token will be added to 'res' by calling 'res['token'] = generate_auth_token(res);'

* Add `Base<endpoint_controller_name>.py` in `src/controllers/__init__.py`:

```python
from src.forms.user_form import\
    UserGetForm

class BaseUserController(BaseController):
    model = UserModel()
    get_form = UserGetForm
```

* Create `<endpoint_name>_controller.py` in this case `user_controller.py`:
This file plays as a request receiver and pass it to model.