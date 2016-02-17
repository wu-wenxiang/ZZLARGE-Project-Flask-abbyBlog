'''
Created on 2016-02-17

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

import json

from flask import Blueprint
from flask import render_template
from flask_restful import Api, Resource

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

class API_Users(Resource):
    def get(self):
        users = User.query.all()
        for user in users:
            user.password = '******'
        return {'users': [toDict(u) for u in users]}

class API_User(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        user.password = '******'
        return {'user': toDict(user)}

api_res.add_resource(API_Users, '/users')
api_res.add_resource(API_User, '/users/<int:id>')