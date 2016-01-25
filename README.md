
[![Build Status][travis-image]][travis-url]
[![Coverage percentage][coveralls-image]][coveralls-url]

#Python-parse
	Python API template for backend system using parse.com as database.

[![image](python-parse.png)](https://github.com/nghiattran/python-parse) 

[Generator](#generator)&nbsp;&nbsp;&nbsp;
[Roadmap](#road-map)&nbsp;&nbsp;&nbsp;
[Basic command](#basic)&nbsp;&nbsp;&nbsp;
[API architecture](#architecture)&nbsp;&nbsp;&nbsp;

#<a name="generator">Generator-python-parse
Now you can use [Generator-python-parse][generator-python-parse-url] to generate entire project and add custom API endpoint.

###Installation
First, install [Yeoman](http://yeoman.io) and generator-python-parse using [npm](https://www.npmjs.com/) (we assume you have pre-installed [node.js](https://nodejs.org/)).

```bash
npm install -g yo
npm install -g generator-python-parse
```

###Usage
```bash
yo python-parse				#To generate entire project
yo python-parse:app 		#To add an endpoint
```

#<a name="road-map">Road map

List of planning features:

- [x] Limit request per IP
- [x] Limit request per interval of time
- [x] Email automation
- [x] Social network integration
- [x] Integrate with yeoman


#<a name="basic"></a>Basic command

###Installation
    
    # install all dependencies
    bin/install
 
###Start
   
    #start api at port 8000
    bin/start
    
###Testing
    
    # run tests
    bin/test
    # or run a specific test file
    bin/test path/to/file

    # run coverage
    bin/cover

    # clean up
    bin/clean

#<a name="architecture">API architecture

    bin
        \- install                          # install all dependencies
        \- start_redis                      # start redis
        \- start                            # start service   
        \- test                             # run tests
        \- cover                            # run coverage
        \- clean                            # clean coverage
    app.py                                  # create app and set up endpoints 
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

####1/ Create `<endpoint_name>_form.py` in this case `user_form.py`:
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

####2/ Create `<endpoint_name>_model.py` in this case `user_model.py`:
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

####3/ Add `Base<endpoint_controller_name>.py` in `src/controllers/__init__.py`:

```python
from src.forms.user_form import\
    UserGetForm

class BaseUserController(BaseController):
    model = UserModel()
    get_form = UserGetForm
```

####4/ Create `<endpoint_name>_controller.py` in this case `user_controller.py`:
This file plays as a request receiver and pass it to model. 
```python
import json
from src.controllers import\
    BaseUserController
from src.models.authentication_model import\
    requires_auth,\
    limit
    
class UsersController(BaseUserController):
    # Require authentication token
    @requires_auth
    # Limit number of requests per IP
    @limit(requests=100, window=30, by='ip', group=None)
    # Limit number of requests per second
    @limit(requests=30, window=1, by='parse', group='parse')
    def get(self):
        form = self.get_form()
        params = form.data

        res = self.model.get(
            collection='users',
            params=params)
        return res


class UserController(BaseUserController):
    @requires_auth
    @limit(requests=100, window=30, by='ip', group=None)
    @limit(requests=30, window=1, by='parse', group='parse')
    def get(self, object_id):
        where = {
            'objectId': object_id
        }
        params = {
            'where': json.dumps(where)
        }
        res = self.model.get(
            collection='users',
            params=params)
        return res

    @requires_auth
    @limit(requests=100, window=30, by='ip', group=None)
    @limit(requests=30, window=1, by='parse', group='parse')
    def put(self, object_id):
        form = self.put_form()
        payload = form.data

        res = self.model.put(
            collection='users',
            object_id=object_id,
            payload=payload,
            master_key=True)
        return res
```

`@requires_auth` will check if the request has `authentication` token. If not, return error.

`@limit(requests=100, window=30, by='ip', group=None)` if the number of requests sent from an IP to an endpoint `group` is greater than `request_limit` in time interval `window`. If it is, return error.

`@limit(requests=30, window=1, by='parse', group='parse')` if the number of requests exceed capability of the server. If it does, return error.

####5/ Create endpoint and its associate controller
Just simply add the followings to app.py

```python
api.add_resource(UsersController, 'users')
api.add_resource(UserController, 'users/<string:object_id>')
```

Where `UsersController` is the controller to handle `users` endpoint and `UserController` handles `users/<string:object_id>`.

#License
&nbsp;&nbsp;&nbsp;[License](https://github.com/nghiattran/LICENSE)

#Credits
[Kien Pham](https://github.com/kienpham2000)

[python-parse-url]: https://github.com/nghiattran/python-parse
[generator-python-parse-url]: https://github.com/nghiattran/generator-python-parse
[travis-url]: https://travis-ci.org/nghiattran/python-parse
[travis-image]: https://travis-ci.org/nghiattran/python-parse.svg?branch=master
[coveralls-image]: https://coveralls.io/repos/nghiattran/python-parse/badge.svg
[coveralls-url]: https://coveralls.io/r/nghiattran/python-parseiattran/LICENSE)

#Credits
[Kien Pham](https://github.com/kienpham2000)