from mylib import app
from flask import flash, redirect, render_template, request
from werkzeug.security import check_password_hash, generate_password_hash
from mylib.models import Users, Titles, Authors, Publishers

@app.route("/")
def index():
    # TODO create login authentication
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_username = request.form["username"]
        new_email = request.form["email"]
        new_password = request.form["password"]

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