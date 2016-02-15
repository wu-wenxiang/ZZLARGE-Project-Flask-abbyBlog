'''
Created on 2016-01-17

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

from flask import Blueprint
from flask import render_template
from edustack.models import User

home = Blueprint('home', __name__)

@home.route('/')
@home.route('/index/')
def hello():
    admin = User.query.filter_by(name='admin').first()
    return render_template(r"home/layout.html", user=admin)