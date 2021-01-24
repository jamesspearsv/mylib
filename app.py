import os
from tempfile import mkdtemp

from flask import Flask, flash, redirect, render_template, request, session, json, jsonify, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy

from helper import login_required


app = Flask(__name__)

#setup sqlalcemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalogs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Configure flask-session
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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
    name = Users.query.filter_by(id=session["user_id"]).first()
    return render_template("index.html", name=name.username)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_username = request.form["username"]
        new_email = request.form["email"]
        new_password = request.form["password"]
        password_confirmation = request.form.get("confirmation")

        if not new_username or not new_email or not new_password:
            flash("Please complete all fields.")
            return render_template("register.html")
        if Users.query.filter_by(username=new_username).first():
            flash("Username unavailable")
            return render_template("register.html")
        if password_confirmation != new_password:
            flash(" Passwords must match")
            return render_template("register.html")

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

        # clear session 
        session.clear()

        user = request.form["username"]
        password = request.form["password"]

        rows = Users.query.filter_by(username=user).all()
        print(rows)
        if len(rows) != 1:
            return "Invalid Username"
        if not check_password_hash(rows[0].hashword, password):
            return "Invalid password"
        else:
            session["user_id"] = rows[0].id
            print("User {}".format(session["user_id"]))
            return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    # Clear session
    session.clear()

    return redirect("/")

@app.route("/flash")
def message():
    flash('This is a message!')
    return redirect("/")

# Driver code
if __name__ == '__main__':
    app.run(debug=True)