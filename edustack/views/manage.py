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
from edustack.views.home import _get_page_index

manage = Blueprint('manage', __name__)

@manage.before_request
def before_request():
    if not (current_user.is_authenticated and current_user.admin):
        return redirect(url_for('home.signin'))

@manage.route('/blogs/create/')
def manage_blogs_create():
    return render_template(r"home/manage_blog_edit.html",
                           action='/api/blogs', redirect='/manage/blogs')
@manage.route('/')
@manage.route('/blogs/')
def manage_blogs():
    return render_template(r"home/manage_blog_list.html",
                           page_index=_get_page_index(),
                           user=current_user)