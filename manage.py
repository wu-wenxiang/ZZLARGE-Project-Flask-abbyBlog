'''
Created on 2016-01-17

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

import logging
import os
import shutil
import subprocess
import sys


BASE_DIR = os.path.dirname(__file__)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("manage.py")
global app

def showUsage():
    print("""Usage:
    python manage.py <Option>
    python manage.py syncdb    # Create DB
    python manage.py init      # Init Demo datas
    python manage.py clean     # Clean virtenv
    python manage.py prepare   # Prepare virtenv
    """)
    sys.exit()

def opt_syncdb():
    from edustack.models import db
    db.drop_all()
    db.create_all()

def opt_init():
    from edustack.models import db
    from edustack.models import User
    adminUser = User("admin", "admin@test.com")
    db.session.add(adminUser)
    db.session.commit()

def opt_clean():
    ENV_DIR = "env"
    if os.path.isdir(ENV_DIR):
        shutil.rmtree(ENV_DIR)

def opt_prepare():
    _assert_cmd_exist("pip")
    os.system("pip install virtualenv")

    INSTANCE_DIR = "instance"
    DEMO_DIR = "demo"
    if not os.path.exists(INSTANCE_DIR):
        os.mkdir(INSTANCE_DIR)
    if not os.path.exists(os.path.join(INSTANCE_DIR, "config.py")):
        shutil.copyfile(os.path.join(DEMO_DIR, "config.py"),
                        os.path.join(INSTANCE_DIR, "config.py"))
    DB_DIR = os.path.join("edustack", "db")
    if not os.path.exists(DB_DIR):
        os.mkdir(DB_DIR)
    if not os.path.exists(os.path.join(DB_DIR, "demo.db")):
        shutil.copyfile(os.path.join(DEMO_DIR, "demo.db"),
                        os.path.join(DB_DIR, "demo.db"))
    LOGS_DIR = "logs"
    if not os.path.exists(LOGS_DIR):
        os.mkdir(LOGS_DIR)

def _assert_cmd_exist(cmd):
    try:
        subprocess.call(cmd)
    except Exception, e:
        log.warning("{}->{}".format(type(e), e.message))
        log.error("Command '{}' not exist!".format(cmd))
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        showUsage()

    selfModule = __import__(__name__)
    optFunName = "opt_" + sys.argv[1].strip()
    if optFunName not in selfModule.__dict__:
        showUsage()

    if BASE_DIR.strip():
        os.chdir(BASE_DIR)
    selfModule.__dict__[optFunName](*sys.argv[2:])
