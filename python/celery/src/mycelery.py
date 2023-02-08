#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/20 22:14
# @Author  : 1823218990@qq.com
# @File    : mycelery.py
# @Software: Pycharm


import sys
import os

cur_path = os.path.dirname(os.path.realpath(sys.argv[0]))
CELERY_DIR = os.path.dirname(cur_path)

sys.path.insert(0, CELERY_DIR)

# print(CELERY_DIR)

from celery import Celery

# conf use
# from src.config import BROKER_URL, CELERY_RESULT_BACKEND

# app = Celery("tasks", broker=BROKER_URL, backend=CELERY_RESULT_BACKEND, include=['src.tasks'])

# config file use
from src import config


app = Celery()
app.config_from_object(config)
app.conf.setdefault("include", ['src.tasks'])
print(app.conf)
# app.conf.timezone = 'Asia/Shanghai'
# app.conf.enable_utc = False
#app.start()
