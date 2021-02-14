# Link to volume on Google Books https://www.google.com/books/edition/_/{googleBooksId}?hl=en

# Import app and db instances from __init__.py
from mylib import app
from mylib import db

# Import Dtatbase models and helper functions
from mylib.models import Users, Titles, Authors, Publishers, Catalogs
from mylib.helpers import login_required, googleBooksSearch, googleBooksRetreive

# Import flask functions and security functions
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
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            return "Error"

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
        if not row or not check_password_hash(row.hashword, password):
            flash("Invalid username or password. Please try again")
            return redirect("/login")
        else:
            session["user_id"] = row.id
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
    results = googleBooksSearch(search_term)
    return render_template("search.html", query=search_term, results=results)

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
                return "Error: Author"

        # Check is publisher is in Publishers table
        if not Publishers.query.filter_by(publisherName=catalogRecord["publisher"]).first():
            # TODO add publisher to Publisher table
            new_publisher = Publishers(publisherName=catalogRecord["publisher"])

            try:
                db.session.add(new_publisher)
                db.session.commit()
            except:
                return "Error: Publisher"

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
                return "Error: Title"

        if not Catalogs.query.filter_by(userId=session["user_id"], titleId=Titles.query.filter_by(title=catalogRecord["title"]).first().id).first():
            new_record = Catalogs(format=request.form.get("format"), userId=session["user_id"], 
            titleId=Titles.query.filter_by(title=catalogRecord["title"]).first().id)

            try:
                db.session.add(new_record)
                db.session.commit()
                flash(f"Success! Added to your catalog!")
                return redirect("/")
            except:
                return "Error: Catalog"
        
        else: 
            flash(f"Looks like that one's already in your catalog.")
            return redirect("/")
    
    else:
        volumeID = request.args.get("volumeID")

        volumeInfo = googleBooksRetreive(volumeID)

        return render_template("edit.html", volumeInfo=volumeInfo)

@app.route("/test", methods=["POST"])
def test():
    return "POSTED!"