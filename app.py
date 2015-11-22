__author__ = 'nghia'

from flask import\
    Flask
from flask_restful import\
    Api
from app.controllers.test_controller import\
    TestController
from app.controllers.user_controller import \
    UsersController,\
    SignupController, \
    LoginController,\
    ResetpasswordController,\
    UserController


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
