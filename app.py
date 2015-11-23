__author__ = 'nghia'

from flask import\
    Flask
from flask_restful import\
    Api
from src.controllers.test_controller import\
    TestController
from src.controllers.user_controller import \
    UsersController,\
    SignupController, \
    LoginController,\
    ResetpasswordController,\
    UserController
import urllib3
urllib3.disable_warnings()

app = Flask(__name__)
api = Api(app, prefix="/api/")

api.add_resource(TestController, '')

api.add_resource(UsersController, 'users')
api.add_resource(UserController, 'users/<string:objectId>')

api.add_resource(LoginController, 'login')

api.add_resource(SignupController, 'signup')

api.add_resource(ResetpasswordController, 'resetpassword')

if __name__ == '__main__':
    app.run(debug=True)
