'''
Created on 2016-01-13

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

import os

DEBUG = True
BCRYPT_LEVEL = 12
MAIL_FROM_EMAIL = "robert@example.com"

SECRET_KEY = 'oHBvtkuTs7OThYCpVTZok6pf2wUk'
STRIPE_API_KEY = 'x2NA6wvyZhJ9DYHCeCrTxHIHnShyuF7dbuX4'
SQLALCHEMY_DATABASE_URI = 'sqlite:///demo/demo.db'

ACCEPT_LANGUAGES = ['en_US', 'zh_Hans_CN']
BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'

SQLALCHEMY_TRACK_MODIFICATIONS = True

LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
DEBUG_LOG = os.path.join(LOG_DIR, 'debug.log')
ERROR_LOG = os.path.join(LOG_DIR, 'error.log')

THEME = 'default'