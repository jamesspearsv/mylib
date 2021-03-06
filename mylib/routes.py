# Link to volume on Google Books https://www.google.com/books/edition/_/{googleBooksId}?hl=en

# Import app and db instances from __init__.py
from mylib import app
from mylib import db

# Import Dtatbase models and helper functions
from mylib.models import Users, Titles, Authors, Publishers, Catalogs
from mylib.helpers import googleBooksSearch, googleBooksRetreive

# Import flask functions and security functions
from flask import flash, redirect, render_template, request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash

# imports from flask-login
from flask_login import login_user, login_required, logout_user, current_user


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        title = request.form.get("titleId")
        user = current_user.id

        record = Catalogs.query.filter_by(titleId=title, userId=user).first()

        try:
            db.session.delete(record)
            db.session.commit()
        except:
            # Internal error. Abort and throw 500 error
            return "Error: Delete"

        flash("Successfully deleted record from your catalog!")
        return redirect("/")
    else:

        name = Users.query.get(current_user.id)

        # Retreives catalog info from database
        catalog = (db.session.query(Titles.title, Titles.subtitle, Titles.ISBN, Titles.publicationDate, Titles.cover,
                Titles.pagination, Titles.googleBooksId, Authors.authorName, Publishers.publisherName, Catalogs.format, Titles.id)
                .join(Authors, Publishers, Catalogs).order_by(Titles.title)
                .filter(Catalogs.userId==current_user.id)).all()

        return render_template("index.html", name=name.username, catalog=catalog)


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
        except:
            return "Error: Adding user"

        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        # clear user session
        logout_user()

        # Grab user input from posted login form
        user = request.form["username"]
        password = request.form["password"]

        # If entered data matches a username in DB
        user = Users.query.filter_by(username=user).first()
        if user:
            # If password is incorrect
            if not check_password_hash(user.hashword, password):
                flash("Invalid password.")
                return redirect("/login")
            else:
                login_user(user)
                return redirect("/")

        # Else check if entered data matched an email in DB
        user = Users.query.filter_by(email=user).first()
        if user:
            # If password is incorrect
            if not check_password_hash(user.hashword, password):
                flash("Invalid password.")
                return redirect("/login")
            else:
                login_required(user)
                return redirect("/")

        # If entered data matches neither a username or an email in DB
        flash ("Invalid username or email")
        return redirect("/login")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    # Clear session
    logout_user()
    return redirect("/login")

@app.route("/search")
@login_required
def search():

    # Gets input from search box and return serch.html with user search term
    search_term = request.args.get("search")
    page_number = request.args.get("page_number")

    if search_term == None or search_term == "":
        flash("Please enter a search term")
        return redirect("/")
    results = googleBooksSearch(search_term, page_number)
    return render_template("search.html", query=search_term, results=results, page_number=page_number)

@app.route("/volume")
@login_required
def volume():
    if request.method == "POST":
        return "TODO"

    else:
        
        volumeId = request.args.get("volumeId")
        volumeInfo = googleBooksRetreive(volumeId)
        
        return render_template("volume.html", volumeInfo=volumeInfo)

@app.route("/add", methods=["POST"])
@login_required
def add():
    if request.method == "POST":

        # Grab volume info from Google Books
        catalogRecord = googleBooksRetreive(request.form.get("volumeId"))


        # Check if author is in Authors table
        if not Authors.query.filter_by(authorName=catalogRecord["authors"][0]).first():
            # TODO add author to Authors table
            new_author = Authors(authorName=catalogRecord["authors"][0])

            try:
                db.session.add(new_author)
                db.session.commit()
            except:
                return "Author"

        # Check is publisher is in Publishers table
        if not Publishers.query.filter_by(publisherName=catalogRecord["publisher"]).first():
            # add publisher to Publisher table
            new_publisher = Publishers(publisherName=catalogRecord["publisher"])

            try:
                db.session.add(new_publisher)
                db.session.commit()
            except:
                return "Publisher"

        # Check if title is Titles table already
        if not Titles.query.filter_by(title=catalogRecord["title"]).first():
            # get author and publisher IDs
            author = Authors.query.filter_by(authorName=catalogRecord["authors"][0]).first()
            publisher = Publishers.query.filter_by(publisherName=catalogRecord["publisher"]).first()

            new_title = Titles(title=catalogRecord["title"], subtitle=catalogRecord["subtitle"],
            ISBN=catalogRecord["ISBN"], publicationDate=catalogRecord["publishedDate"], cover=catalogRecord["cover"],
            pagination=catalogRecord["pageCount"], googleBooksId=catalogRecord["googleBooksId"], authorId=author.id, publisherId=publisher.id)

            try:
                db.session.add(new_title)
                db.session.commit()
            except:
                return "Title"

        # Check if title in currently in user's catalog
        if not Catalogs.query.filter_by(userId=current_user.id, titleId=Titles.query.filter_by(title=catalogRecord["title"]).first().id).first():
            new_record = Catalogs(format=request.form.get("format"), userId=current_user.id,
            titleId=Titles.query.filter_by(title=catalogRecord["title"]).first().id)

            try:
                db.session.add(new_record)
                db.session.commit()
                flash("Succesfully added to your catalog!")
                return redirect("/")
            except:
                return "Catalog"

        else:
            flash("Looks like that one's already in your catalog.")
            return redirect("/")

    else:
        volumeID = request.args.get("volumeID")

        volumeInfo = googleBooksRetreive(volumeID)

        return render_template("edit.html", volumeInfo=volumeInfo)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/account")
@login_required
def account():
    # Retreive user information from DB
    row = Users.query.get(current_user.id)

    user = {
        "id": row.id,
        "username": row.username,
        "email": row.email,
    }

    return render_template("account.html", user=user)


@app.route("/account/username", methods=["POST"])
@login_required
def editUsername():
    # If password is incorrect
    if not check_password_hash(Users.query.get(current_user.id).hashword, request.form.get('password')):
        flash("Invalid password")
        return redirect("/account")
    else:
        # get user info and update
        user = Users.query.get(current_user.id)
        try:
            user.username = request.form.get("username")
            print(user.username)
            db.session.commit()
            flash("Successfully updated username!")
            return redirect("/account")
        except:
            return "Error: Updating username"


@app.route("/account/email", methods=["POST"])
@login_required
def editEmail():
    # If password is incorrect
    if not check_password_hash(Users.query.get(current_user.id).hashword, request.form.get('password')):
        flash("Invalid password")
        return redirect("/account")
    else:
        # Get user info and update
        user = Users.query.get(current_user.id)
        try:
            user.email = request.form.get("email")
            db.session.commit()
            flash("Successfully updated email!")
            return redirect("/account")
        except:
            return "Error: Updating email"


@app.route("/account/password", methods=["POST"])
@login_required
def editPassword():
    if not check_password_hash(Users.query.get(current_user.id).hashword, request.form.get('password')):
        flash("Invalid password")
        return redirect("/account")
    else:
        # Get entered data and check against password requirements
        newPassword = request.form.get("newPassword")

        reqs = {
            "length": False,
            "digit": False,
            "upperCase": False
        }

        for letter in newPassword:
            if letter.isupper():
                reqs["upperCase"] = True
            if letter.isdigit():
                reqs["digit"] = True
        if len(newPassword) >= 6:
            reqs["length"] = True

        # If password meets requirements, update database
        if reqs["length"] == True and reqs["digit"] == True and reqs["upperCase"] == True:
            user = Users.query.get(current_user.id)
            newHashword = generate_password_hash(newPassword)


            try:
                user.hashword = newHashword
                db.session.commit()
                flash("Successfully updated your password!")
                return redirect("/account")
            except:
                return "Error: Updating password"


        else:
            flash("Password requirements not meet. Your password was not changed. Please try agin.")
            return redirect("/account")

@app.route("/account/delete", methods=["POST"])
@login_required
def delete():
    enteredUsername = request.form.get("username")
    enteredPassword = request.form.get("password")

    # Get user's info from database
    user = Users.query.get(current_user.id)

    # if entered username is incorrect
    if enteredUsername != user.username:
        flash("Invalid username.")
        return redirect("/account")
    # if entered password is incorrect
    elif not check_password_hash(user.hashword, enteredPassword):
        flash("Invalid password.")
        return redirect("/account")
    else:
        # Grab all user's catalog records to delete
        catalog = Catalogs.query.filter_by(userId=current_user.id).all()
        for item in catalog:
            try:
                db.session.delete(item)
                db.session.commit()
            except:
                pass

        # Delete user
        try:
            db.session.delete(user)
            db.session.commit()
        except:
            return "Error: Deleting account"

        return redirect("/logout")


@app.route("/details")
@login_required
def edtails():
    bookId = request.args.get("q")
    
    # Retreives catalog info from database
    record = (db.session.query(Titles.title, Titles.subtitle, Titles.ISBN, Titles.publicationDate, Titles.cover,
    Titles.pagination, Titles.googleBooksId, Authors.authorName, Publishers.publisherName, Catalogs.format, Titles.id)
    .join(Authors, Publishers, Catalogs)
    .filter(Titles.id == bookId, Catalogs.userId==current_user.id)).first()

    #volumeInfo = googleBooksRetreive(record.googleBooksId)

    return render_template("details.html", record=record)


# Error handelers for 404 not found and 500 internal server error
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500
