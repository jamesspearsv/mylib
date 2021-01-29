from mylib import db
from flask_sqlalchemy import SQLAlchemy


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