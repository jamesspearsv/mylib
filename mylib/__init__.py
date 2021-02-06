## File the initializes FLask App
## Watch for circular imports from rest of module
## Create app, db, and other instances that will be used
## in routes, models, etc first. Then import routes

# Import flask
from flask import Flask

# Import flask-session and needed library
from flask_session import Session
from tempfile import mkdtemp

# Import flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# create flask app
app = Flask(__name__)

#setup and initialize sqlalcemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalogs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure flask-session for user authenticaton
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Import app routes after creating app
from mylib import routes

# Create DB is it doesn't already exist
try:
    db.create_all()
except:
    pass