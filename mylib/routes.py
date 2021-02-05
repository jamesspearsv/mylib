# Import app and db instances from __init__.py
from mylib import app
from mylib import db

# 
from mylib.models import Users, Titles, Authors, Publishers
from mylib.helpers import login_required, lookup, getVolumeInfo

from flask import flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash


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

        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")

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
    
    # Gets input from search box and return serch.html with user search term
    search_term = request.args.get("search")
    if search_term == None or search_term == "":
        return "Error" # TODO create error html page
    results = lookup(search_term)
    return render_template("search.html", query=search_term, results=results)

@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if request.method == "POST":
        # Grab volume information from posted form
        # TODO if author0, title empty then return error
        # TODO grab other fields from form
        authors = []
        for i in range(10):
            # Checks it author field exists
            if not request.form.get(f"{i}"):
                break
            # appends author name to authors list
            authors.append(request.form.get(f"{i}"))

        # TODO check if publisher or authors are already in DB.
            # if yes then get authorId and publisherId
            # else add publisher and author to DB
        # TODO Add title to DB
        # TODO add title to user's catalog.
        
        print(authors)
        return "TODO"
    else:
        volumeID = request.args.get("volumeID")

        volumeInfo = getVolumeInfo(volumeID)

        return render_template("edit.html", volumeInfo=volumeInfo)

@app.route("/test", methods=["POST"])
def test():
    return "POSTED!"