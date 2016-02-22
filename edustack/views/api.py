'''
Created on 2016-02-17

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

import flask_login as login
import markdown2
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
from edustack.models import Page
from edustack.models import Comment
from flask_login import current_user


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
class API_Auth(Resource):
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

def _get_blogs_by_page(pageIndex):
    total = Blog.query.count()
    page = Page(total, pageIndex)
    blogs = Blog.query.offset(page.offset).limit(page.limit)
    return blogs, page

getBlogsList = ['page', 'format']
getBlogsParser = reqparse.RequestParser()
[getBlogsParser.add_argument(i) for i in getBlogsList]
postBlogsList = ['name', 'summary', 'content']
postBlogsParser = reqparse.RequestParser()
[postBlogsParser.add_argument(i) for i in postBlogsList]
class API_Blogs(Resource):
    def get(self):
        args = getBlogsParser.parse_args()

        page = 1
        try:
            page = int(args['page'])
        except:
            pass
        format = args['format']

        blogs, page = _get_blogs_by_page(page)
        if format=='html':
            for blog in blogs:
                blog.content = markdown2.markdown(blog.content)
        return dict(blogs=[toDict(i) for i in blogs], page=page.toDict())

    def post(self):
        if not (current_user.is_authenticated and current_user.admin):
            abort(403, "No Permission!")
        args = postBlogsParser.parse_args()
        assertArgsNotEmpty(args, postBlogsList)

        name = args['name'].strip()
        summary = args['summary'].strip()
        content = args['content'].strip()

        if not name:
            abort(400, message="name can not be empty!")
        if not summary:
            abort(400, message="summary can not be empty!")
        if not content:
            abort(400, message="content can not be empty!")

        blog = Blog(current_user.id, name, summary, content)
        db.session.add(blog)
        db.session.commit()
        return {'blog': toDict(blog)}

api_res.add_resource(API_Users, '/users')
api_res.add_resource(API_User, '/users/<int:id>')
api_res.add_resource(API_Auth, '/authenticate')
api_res.add_resource(API_Blogs, '/blogs')
