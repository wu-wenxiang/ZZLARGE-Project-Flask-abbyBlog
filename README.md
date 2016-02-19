# AbbyBlog
An elegant blog 

[Demo Online](http://wuwenxiang.cloudapp.net)

    admin: admin@admin.com / admin@admin.com
    test1: test1@test.com / test1@test.com
    test2: test2@test.com / test2@test.com

Run locol demo service

    ./start.sh
    ./start.sh -f # To force rebuild virtual environment

Run testcases

    ./run_test.sh

Create database

    python manage.py syncdb
