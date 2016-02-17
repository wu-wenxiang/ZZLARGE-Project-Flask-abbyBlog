'''
Created on 2016-01-13

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

import datetime

from flask_sqlalchemy import SQLAlchemy
from edustack import wsgiApp

db = SQLAlchemy(wsgiApp)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)
    image = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    blogs = db.relationship('Blog', backref='user', lazy='dynamic')
#     comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def __init__(self, name, email, password, image, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.image = image
        self.admin = admin

    def __repr__(self):
        return '<User {!r}>'.format(self.name)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(50))
    summary = db.Column(db.String(50))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, user_id, name, summary, content):
        self.user_id = user_id
        self.name = name
        self.summary = summary
        self.content = content

    def __repr__(self):
        return '<Blog {!r}>'.format(self.name)

# class Comment(Model):
#     __table__ = 'comments'
# 
#     id = CharField(primary_key=True, default=next_id, max_length=50)
#     blog_id = CharField(max_length=50)
#     user_id = CharField(max_length=50)
#     user_name = CharField(max_length=50)
#     user_image = CharField(max_length=500)
#     content = TextField()
#     created_at = FloatField(default=time.time)


# class LocalAuth(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     password = db.Column(db.String(120))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('User',
#         backref=db.backref('localauth', uselist=False))
# 
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password
# 
#     def __repr__(self):
#         return '<LocalAuth {!r}>'.format(self.username)