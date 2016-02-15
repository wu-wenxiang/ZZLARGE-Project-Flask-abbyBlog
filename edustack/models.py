'''
Created on 2016-01-13

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

from flask_sqlalchemy import SQLAlchemy
from edustack import wsgiApp

db = SQLAlchemy(wsgiApp)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User {!r}>'.format(self.name)

class LocalAuth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('localauth', uselist=False))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<LocalAuth {!r}>'.format(self.username)