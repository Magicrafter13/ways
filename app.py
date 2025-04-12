"""Multi-service video broadcast creator."""

import secrets

from icecream import ic
from flask import Flask, redirect, render_template, request, session
from flask_login import login_user, login_required, LoginManager, UserMixin
from flask_restful import Api, Resource

app = Flask(__name__)
app.secret_key = secrets.token_hex()
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

details = {
    'title': 'TITLE',
    'short-title': '',

}

# Authentication

users = { '0': { 'password': 'password' } }

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(id):
    if id not in users:
        return

    user = User()
    user.id = id
    return user

#@login_manager.request_loader
#def request_loader(request):
#    """Load user from flask request."""
#    user = User()
#    user.id = 0
#    return user

#@login_manager.unauthorized_handler
#def unauthorized_handler():
#    """Login failure."""
#    return 'Unauthorized', 401

class StreamDetailsManager(Resource):
    @login_required
    def get(self):
        return details
    @login_required
    def put(self):
        data = request.get_json()
        if 'title' in data:
            details['title'] = data['title'].strip()
        return details

api.add_resource(StreamDetailsManager, '/details/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login landing page."""
    if request.method == 'GET':
        return render_template('login.html')
    
    # POST
    password = request.form['password']
    if users['0']['password'] == password:
        user = User()
        user.id = '0'
        login_user(user)
        return redirect('/')

    return 'Unable to authenticate!'

@app.route('/')
@login_required
def index():
    """Stream details management page."""
    return render_template('index.html')

application=app  # for uWSGI
