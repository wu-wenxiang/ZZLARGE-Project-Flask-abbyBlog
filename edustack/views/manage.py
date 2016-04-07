'''
Created on 2016-02-19

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

from flask import Blueprint
from flask import render_template, url_for, abort
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

@manage.route('/blogs/edit/<int:blog_id>')
def manage_blogs_edit(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if not blog:
        abort(404)
    return render_template(r"home/manage_blog_edit.html",
                           id = blog.id,
                           name = blog.name,
                           summary = blog.summary,
                           content = blog.content,
                           action='/api/blogs/{0}'.format(blog_id),
                           redirect='/manage/blogs')

@manage.route('/blogs/')
def manage_blogs():
    return render_template(r"home/manage_blog_list.html",
                           page_index=_get_page_index(),
                           user=current_user)

@manage.route('/')
@manage.route('/comments/')
def manage_comments():
    return render_template(r"home/manage_comment_list.html",
                           page_index=_get_page_index(),
                           user=current_user)

@manage.route('/users/')
def manage_users():
    return render_template(r"home/manage_user_list.html",
                           page_index=_get_page_index(),
                           user=current_user)

