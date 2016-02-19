'''
Created on 2016-02-19

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

from flask import Blueprint
from flask import render_template, url_for
from flask_login import current_user, redirect
from edustack.models import User
from edustack.models import Blog
from edustack.models import Comment

manage = Blueprint('manage', __name__)

@manage.before_request
def before_request():
    if not (current_user.is_authenticated and current_user.admin):
        return redirect(url_for('home.signin'))

@manage.route('/')
def hello():
    users = User.query.all()
    blogs = Blog.query.all()
    comments = Comment.query.all()
    return render_template(r"test/smoketest.html",users=users,
                           blogs=blogs, comments=comments)