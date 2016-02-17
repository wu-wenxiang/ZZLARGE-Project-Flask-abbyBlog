'''
Created on 2016-01-13

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

import datetime
import jinja2_filters
import os
import time
from flask import Flask
from inspect import getmembers
from inspect import isfunction


def create_app():
    try:
        app = Flask(__name__, instance_relative_config=True)
    except IOError:
        app = Flask(__name__)
    app.config.from_object('config.default')
    app.config.from_pyfile('config.py')
    try:
        app.config.from_envvar('APP_CONFIG_FILE')
    except RuntimeError:
        pass
    
    customFilters = {name: function 
                  for name, function in getmembers(jinja2_filters)
                  if isfunction(function)}
    app.jinja_env.filters.update(customFilters)

    return app

wsgiApp = create_app()

from edustack.views import home
from edustack.views import test
from edustack.views import api
wsgiApp.register_blueprint(home, url_prefix="/")
wsgiApp.register_blueprint(home, url_prefix="/home")
wsgiApp.register_blueprint(test, url_prefix="/test")
wsgiApp.register_blueprint(api, url_prefix="/api")

