#!/opt/midware/python3.8/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/12/20 22:17
# @Author  : 1823218990@qq.com
# @File    : run_tasks.py
# @Software: Pycharm
from random import randint
import sys
import os


cur_path = os.path.dirname(os.path.realpath(sys.argv[0]))
CELERY_DIR = os.path.dirname(cur_path)

# print(CELERY_DIR)
sys.path.insert(0, CELERY_DIR)
sys.path.insert(1, os.path.join(CELERY_DIR, 'lib/python3.8/site-packages'))

# 2023 02 16
from celery.result import AsyncResult
from src.mycelery import app

from src.tasks import cal_sum, mytask
from datetime import datetime


res2 = cal_sum.apply_async((randint(1, 10),))
print(res2.id)


res3 = mytask.apply_async((randint(1, 10), randint(1, 10),), priority=0)
print(res3.id)


# res1 = cal_sum.delay(10)
tz = datetime.utcnow()
res1 = cal_sum.apply_async((10,), eta=tz, utc=True)
print(res1.id)

async_result = AsyncResult(res1.id, app=app)
data1 = async_result.get()    # 阻塞等待结果
print("data1: {}".format(data1))