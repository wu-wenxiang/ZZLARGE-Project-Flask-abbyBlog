'''
Created on 2016-02-17

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

import flask_login as login
import hashlib
import json
import re

from flask import Blueprint
from flask_restful import Api, Resource
from flask_restful import abort
from flask_restful import reqparse

from edustack.models import db
from edustack.models import User
from edustack.models import Blog
from edustack.models import Comment


api = Blueprint('api', __name__)
api_res = Api(api)

def isJsonable(obj):
    try:
        json.dumps(obj)
    except:
        return False
    return True

def toDict(obj):
    return {k:v for k,v in obj.__dict__.items()
            if isJsonable(v)}

def assertArgsNotEmpty(args, keys):
    [abort(400, message="Arg <{0}> Error!".format(i))
     for i in keys if (not args[i]) or (not args[i].strip())]

def abortValueError(name):
    abort(400, message="Arg <{0}> Error!".format(name))

postUserList = ['name', 'email', 'password']
postUserParser = reqparse.RequestParser()
for i in postUserList:
    postUserParser.add_argument(i)

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')

class API_Users(Resource):
    def get(self):
        users = User.query.all()
        for user in users:
            user.password = '******'
        return {'users': [toDict(u) for u in users]}
    def post(self):
        args = postUserParser.parse_args()
        assertArgsNotEmpty(args, postUserList)

        name = args['name'].strip()
        email = args['email'].strip().lower()
        password = args['password']

        if not _RE_EMAIL.match(email):
            abortValueError('email')
        if not _RE_MD5.match(password):
            abortValueError('password')

        user = User.query.filter_by(email=email).first()
        if user:
            abort(400, message="Email is already in use.")

        user = User(name=name, email=email, password=password,
                    image='http://www.gravatar.com/avatar/{0}?d=mm&s=120'
                    .format(hashlib.md5(email).hexdigest()))

        db.session.add(user)
        db.session.commit()
        login.login_user(user)

        user.password = '******'
        return {'user': toDict(user)}

class API_User(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        user.password = '******'
        return {'user': toDict(user)}

postAuthList = ['email', 'password', 'remember']
postAuthParser = reqparse.RequestParser()
for i in postAuthList:
    postAuthParser.add_argument(i)
class API_AUTH(Resource):
    def post(self):
        args = postAuthParser.parse_args()
        assertArgsNotEmpty(args, postAuthList)

        email = args['email'].strip().lower()
        password = args['password']
        remember = True if args['remember']=='true' else False

        user = User.query.filter_by(email=email).first()
        if not user:
            abort(401, message="Invalid email.")
        elif password != user.password:
            abort(401, message="Invalid password.")

        login.login_user(user, remember=remember)

        user.password = '******'
        return {'user': toDict(user)}

api_res.add_resource(API_Users, '/users')
api_res.add_resource(API_User, '/users/<int:id>')
api_res.add_resource(API_AUTH, '/authenticate')
