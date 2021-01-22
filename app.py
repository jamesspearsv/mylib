import os
from flask import Flask, flash, redirect, render_template, request, session, json, jsonify, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

#connect to sqlite database TODO setup sqlalcemy


@app.route("/")
def index():
    # TODO create login authentication
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        print(username)
        print(email)
        print(password)

        # TODO insert info into database with sqlalchemy

        return redirect("/login")
    else: 
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        return "TODO"
    else:
        return render_template("login.html")
