'''
Created on 2016-01-17

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

from flask import Blueprint
from flask import render_template
from edustack.models import User
from edustack.models import Blog
from edustack.models import Comment

test = Blueprint('test', __name__)

@test.route('/')
@test.route('/smoketest/')
def hello():
    users = User.query.all()
    blogs = Blog.query.all()
    comments = Comment.query.all()
    return render_template(r"test/smoketest.html",users=users,
                           blogs=blogs, comments=comments)