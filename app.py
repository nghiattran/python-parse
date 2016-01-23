from flask import\
    Flask, render_template
from flask_restful import\
    Api
from flask.ext.cors import CORS
from src.controllers.user_controller import \
    UsersController,\
    SignupController, \
    LoginController,\
    ResetpasswordController,\
    UserController,\
    AuthController, \
    UserActivationController
import redis
import jinja2

app = Flask(__name__, static_folder='src/static')
# set path to custom templates folder
app.jinja_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader('src/templates'),
])


# set up redis
app.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
app.debug = True

# allow CORS so that localhost:8000 can talk with localhost:9000
CORS(app)

# initial for api
api = Api(app, prefix="/api/")

api.add_resource(UsersController, 'users')
api.add_resource(UserController, 'users/<string:object_id>')

api.add_resource(LoginController, 'login')

api.add_resource(SignupController, 'signup')

api.add_resource(ResetpasswordController, 'resetpassword')

api.add_resource(AuthController, 'auth')

api.add_resource(UserActivationController, 'activate/<string:object_id>')

@app.route('/activated/<string:object_id>')
def activated(object_id):
    return render_template("activated.html")

@app.errorhandler(404)
def page_not_found(e):
    return {'error': 'Page not found', 'code': 404}

if __name__ == '__main__':
    app.run(debug=True)
