#!/opt/midware/python3.8/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/12/20 20:34
# @Author  : 1823218990@qq.com
# @File    : task.py
# @Software: Pycharm
from time import sleep
import sys
import os
cur_path = os.path.dirname(os.path.realpath(sys.argv[0]))
CELERY_DIR = os.path.dirname(cur_path)

sys.path.insert(0, CELERY_DIR)
from src.mycelery import app
from celery import Task


class MyTask(Task):

    # 任务失败时执行
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} on_failure: {1!r}'.format(task_id, exc))

    # 任务成功时执行
    def on_success(self, retval, task_id, args, kwargs):
        print("{} {} on_success".format(task_id, retval))

    # 任务重试时执行
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print("{} {} on_retry".format(task_id, exe))

@app.task
def cal_sum(count):
    sum = 0
    for i in range(count):
        sum += i
        sleep(1)
    return sum


@app.task(name='mytask')
def mytask(x, y):
    return x**2 + y**2 + 1


@app.task(name='timedtask', base=MyTask)
def timedtask():
    """
    config中使用 name指定的任务名
    * 定时任务会产生一个celerybeat-schedule文件：
        该文件用于存放上次执行结果：
        　　1、如果存在  celerybeat-schedule文件，那么读取后根据上一次执行的时间，继续执行。
        　　2、如果不存在celerybeat-schedule文件，那么会立即执行一次。
        　　3、如果存在  celerybeat-schedule文件，读取后，发现间隔时间已过，那么会立即执行。
    :return:
    """
    import random
    mysum = 0
    for i in range(random.randint(10, 1000)):
        mysum += i ** 2 - 2 * i + 4
    sleep(random.randint(3, 6))
    return mysum