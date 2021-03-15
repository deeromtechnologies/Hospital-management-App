import os
from sqla_wrapper import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///HMS.sqlite3"))  # this connects to a database either on Heroku or on localhost




class register(UserMixin,db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(120), unique=False, nullable=False)
    lastname = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    confirmpassword = db.Column(db.String(120), unique=False, nullable=False)

def __init__(self, id, firstname, lastname, username, email, password, confirmpassword):

    self.id = id
    self.firstname = firstname
    self.lastname = lastname
    self.username = username
    self.email = email
    self.password = password
    self.confirmpassword = confirmpassword

	