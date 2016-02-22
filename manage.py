'''
Created on 2016-01-17

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

import hashlib
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
    from edustack.models import Blog
    from edustack.models import Comment
    def init_user(name, email, admin=False):
        emailHash = hashlib.md5(email).hexdigest()
        password = emailHash
        image = "http://www.gravatar.com/avatar/{0}?d=mm&s=120".format(emailHash)
        return User(name, email, password, image, admin)

    adminUser = init_user("admin", "admin@admin.com", True)
    db.session.add(adminUser)
    test1User = init_user("test1", "test1@test.com")
    db.session.add(test1User)
    test2User = init_user("test2", "test2@test.com")
    db.session.add(test2User)

    for i in range(25):
        blog1 = Blog(1, "Amdin_Blog{0}_Name".format(i),
                     "Admin_Blog{0}_Summary".format(i),
                     ("Admin_Blog{0}_Content\n"*20).format(i))
        db.session.add(blog1)

    comment1 = Comment(2, 2, "Comment_User1_Blog2")
    db.session.add(comment1)
    comment2 = Comment(3, 1, "Comment_User2_Blog1")
    db.session.add(comment2)
    db.session.commit()

def opt_clean():
    ENV_DIR = "env"
    if os.path.isdir(ENV_DIR):
        shutil.rmtree(ENV_DIR)

def opt_test():
    from edustack.models import Blog
    print type(Blog.query.count())

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
