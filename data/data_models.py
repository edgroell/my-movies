"""
Module containing all data models of the app
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)

    def __str__(self):
        return self.username

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    poster_url = db.Column(db.String(100), nullable=False)
    imdb_id = db.Column(db.String(100), nullable=False)
    note = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.title
