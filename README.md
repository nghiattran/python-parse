#Work on prgress

[![Build Status](https://travis-ci.org/nghiattran/python-parse.svg?branch=master)](https://travis-ci.org/nghiattran/python-parse)&nbsp;&nbsp;[![Coverage Status](https://coveralls.io/repos/nghiattran/python-parse/badge.svg?branch=master&service=github)](https://coveralls.io/github/nghiattran/python-parse?branch=master)

#Python-parse
    Python API service for backend system using parse.com as database

[![image](python-parse.png)](https://github.com/nghiattran/python-parse)

[Roadmap](https://github.com/nghiattran/python-parse#road-map)&nbsp;&nbsp;&nbsp;[API architecture](https://github.com/nghiattran/angular-parse/blob/gh-pages/README.md#api-architecture)

#Road map

List of planning features:

- [x] Limit request per ip
- [x] Limit request per interval
- [ ] Email automation
- [ ] Update documentation

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
        