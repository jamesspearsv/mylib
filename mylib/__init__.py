## This file the initializes FLask App

from flask import Flask
import secrets
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Set development mode
DEV_MODE = False

# create flask app
app = Flask(__name__)

# Set Dev mode or Prod mode
if DEV_MODE == True:
    #setup and initialize sqlalcemy database in Dev Mode
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalogs.db'
    app.secret_key = 'DEV_MODE secret key'
    app.debug = True
else:
    #setup and initialize sqlalcemy database in Prod Mode
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.secret_key = os.environ.get('SECRET_KEY')
    app.debug = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure Flask-Login and login_manager
login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.login_messege = ""
login_manager.init_app(app)

# Import app routes after creating app
from mylib import routes
from mylib.models import Users

@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(int(user_id))
