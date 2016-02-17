'''
Created on 2016-01-17

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

from flask import Blueprint
from flask import render_template
from edustack.models import User
from edustack.models import Blog

home = Blueprint('home', __name__)

@home.route('/')
@home.route('/index/')
def hello():
    users = User.query.all()
    blogs = Blog.query.all()
    return render_template(r"home/layout.html", users=users, blogs=blogs)