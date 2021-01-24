from flask import Flask, flash, redirect, render_template, request, session, json, jsonify, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from helper import login_required

app = Flask(__name__)

#TODO setup sqlalcemy database and model
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalogs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

session["user_id"] = None

# SQLAlchemy database models
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    hashword = db.Column(db.String(200), nullable=False)

    # Create function to return stinrg when add new record
    def __repr__(self):
        return '<Username %r>' %self.id

class Titles(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Title %r>' %self.id

class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Title %r>' %self.id

class Publishers(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Title %r>' %self.id



@app.route("/")
@login_required
def index():
    # TODO create login authentication
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_username = request.form["username"]
        new_email = request.form["email"]
        new_password = request.form["password"]

        print(new_username)
        print(new_email)
        print(new_password)

        # Create new_user object
        new_user = Users(username=new_username, 
        email=new_email, hashword=generate_password_hash(new_password))
        
        # Push to database
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
        except:
            return "Something's wrong"

    else: 
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]


        rows = Users.query.filter_by(username=user).all()
        print(rows)
        if len(rows) != 1:
            return "Invalid Username"
        if not check_password_hash(rows[0].hashword, password):
            return "Invalid password"
        else:
            return redirect("/")
        

    else:
        return render_template("login.html")

# Driver code
if __name__ == '__main__':
    app.run(debug=True)