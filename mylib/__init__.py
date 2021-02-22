## File the initializes FLask App
## Watch for circular imports from rest of module
## Create app, db, and other instances that will be used
## in routes, models, etc first. Then import routes

# Import flask
from flask import Flask, session

# Import flask-session and needed library
from flask_session import Session
from tempfile import mkdtemp
import secrets

# Import flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# Set development mode
DEV_MODE = True

# create flask app
app = Flask(__name__)

# Generate secret key
secret = secrets.token_urlsafe(32)
app.secret_key = secret\

# Set Dev mode or Prod mode
if DEV_MODE == True:
    #setup and initialize sqlalcemy database in Dev Mode
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalogs.db'
    app.debug = True
else:
    #setup and initialize sqlalcemy database in Prod Mode
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalogs.db'
    app.debug = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#app.config.update(SESSION_COOKIE_SECURE=True)

# Configure flask-session for user authenticaton (use filesystem, secure cookie attribute=True)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = True
app.config.from_object(__name__)
Session(app)


# Import app routes after creating app
from mylib import routes

# Create DB is it doesn't already exist
try:
    db.create_all()
except:
    pass