# -*- coding:utf-8 -*-
'''
Created on 2016-02-17

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

import datetime

def blogtime(t):
    delta = int((datetime.datetime.now()-t).seconds)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)