import os
from flask import Flask, flash, redirect, render_template, request, session, json, jsonify, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

#connect to sqlite database
db = sqlite3.connect("catalog.db", check_same_thread=False)
try:
    db.execute("CREATE TABLE users (id INTEGER, username TEXT NOT NULL, email TEXT NOT NULL, hash TEXT NOT NULL, PRIMARY KEY(id));")
except: 
    pass

@app.route("/")
def index():
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

        db.execute("INSERT INTO users (username, email, hash) VALUES (?, ?, ?);", (username, email, generate_password_hash(password)))
        db.commit()
        return redirect("/login")
    else: 
        return render_template("register.html")
