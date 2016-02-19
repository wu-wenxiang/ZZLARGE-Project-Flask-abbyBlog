'''
Created on 2016-01-17

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

from flask import Blueprint
from flask import render_template, redirect, url_for
from flask_login import current_user, logout_user
from edustack.models import User
from edustack.models import Blog

home = Blueprint('home', __name__)

@home.route('/')
@home.route('/index/')
def index():
    blogs = Blog.query.all()
    return render_template(r"home/blogs.html", blogs=blogs)

@home.route('/register/')
def register():
    return render_template(r"home/register.html")

@home.route('/signin/')
def signin():
    return render_template(r"home/signin.html")

@home.route('/signout/')
def signout():
    logout_user()
    return redirect(url_for('home.index'))