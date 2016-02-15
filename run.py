'''
Created on 2016-01-13

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

from edustack import wsgiApp
import os
import sys

if len(sys.argv) > 1:
    os.environ['APP_CONFIG_FILE'] = sys.argv[1]

if __name__ == "__main__":
    wsgiApp.run(host="0.0.0.0", port=5000)
else:
    app = wsgiApp