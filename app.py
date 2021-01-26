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
        new_username = request.form.get("username")
        new_email = request.form.get("email")
        new_password = request.form.get("password")
        password_confirmation = request.form.get("confirmation")

        reqs = [0,0]

        # if any form fields are empty
        if not new_username or not new_email or not new_password or not password_confirmation:
            flash("Please complete the form")
            return redirect("/register")

        # Check that username and email are available
        user = Users.query.filter_by(username=new_username).first()
        email = Users.query.filter_by(email=new_email).first()
        if user != None and email != None:
            flash("Username and email are unavailable")
            return render_template("register.html", password=new_password, confirmation=new_password)
        if user != None:
            flash("Username is unavailable")
            return render_template("register.html", email=new_email, password=new_password, confirmation=new_password)
        if email != None:
            flash("Email is unavailable")
            return render_template("register.html", username=new_username, password=new_password, confirmation=new_password)
        
        # Checks that password meets reqs and confirmation matches
        # Password checks are extra security in case users mess with HTML in browser to enable submit button before password reqs are met.
        if new_password != password_confirmation:
            return render_template("register.html")

        for char in new_password:
            if char.isdigit():
                reqs[0] += 1
            if char.isupper():
                reqs[1] += 1
        if reqs[0] < 1 or reqs[1] < 1 or len(new_password) < 6:
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

        row = Users.query.filter_by(username=user).first()
        if row == None or not check_password_hash(row.hashword, password):
            flash("Invalid username or password. Please try again")
            return redirect("/login")
        else:
            session["user_id"] = row.id
            print("User {}".format(session["user_id"]))
            return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    # Clear session
    session.clear()

    return redirect("/")

@app.route("/search")
@login_required
def search():
    # Gets input from search box
    search = request.args.get("search")

    # return serch.html with user search term
    return render_template("search.html", search=request.args.get("search"))

@app.route("/test", methods=["POST"])
def test():
    return "POSTED!"

# Driver code
if __name__ == '__main__':
    app.run(debug=True)