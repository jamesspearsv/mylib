from mylib import db
from flask_sqlalchemy import SQLAlchemy


# SQLAlchemy database models
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    hashword = db.Column(db.String(200), nullable=False)

    # Relationship to Catalogs table
    catalog = db.relationship('Catalogs', backref='user', lazy=True)

    # Create function to return stinrg when add new record
    def __repr__(self):
        return '<Username %r>' %self.id

class Catalogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Foreign keys
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    titleId = db.Column(db.Integer, db.ForeignKey('titles.id'), nullable=False)

    def __repr__(self):
        return '<Catalog: Title %r, User %r>' %self.titleId %self.userId

class Titles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False, unique=True)
    subtitle = db.Column(db.Text)
    ISBN = db.Column(db.String(13), unique=True)
    publicationDate = db.Column(db.String(15))
    cover = db.Column(db.String(200), unique=True)
    pagination = db.Column(db.Integer)
    googleBooksID = db.Column(db.String(100), unique=True, nullable=False)

    # Foreign Keys
    primaryAuthorId = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    secondaryAuthorId = db.Column(db.Integer, db.ForeignKey('authors.id'))
    publisherId = db.Column(db.Integer, db.ForeignKey('publishers.id'))

    # Relationship to catalogs table
    catalog = db.relationship('Catalogs', backref='title', lazy=True)

    def __repr__(self):
        return '<Title %r>' %self.id

class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    authorName = db.Column(db.String(200), nullable=False, unique=True)

    # Relationship to titles table
    titlesAuthored = db.relationship('Titles', backref='author', foreign_keys=[Titles.primaryAuthorId], lazy=True)

    def __repr__(self):
        return '<Title %r>' %self.id

class Publishers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publisherName = db.Column(db.String(200), nullable=False, unique=True)

    # Relationship to titles table
    titlesPublished = db.relationship('Titles', backref="publisher", lazy=True)

    def __repr__(self):
        return '<Title %r>' %self.id 