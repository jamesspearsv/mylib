import os


from flask import Flask, flash, redirect, render_template, request, session, json, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

@app.route("/")
def index():
    return "TODO"