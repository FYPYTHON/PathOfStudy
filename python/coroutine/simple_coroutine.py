# coding=utf-8
# 1 - yield
from datetime import datetime
import time
MAX_COUT = 10

# 2 - gevent 网络 i/o操作
# yum search libffi-dev
# pip install gevent
from gevent import monkey
import gevent
import random


class YieldCoroutine(object):
    def __init__(self):
        self.sleep_time = 3

    def work1(self):
        while True:
            print("{}---work1 is run---".format(datetime.now()))
            yield
            time.sleep(self.sleep_time)

    def work2(self):
        while True:
            print("{}---work2 is run---".format(datetime.now()))
            yield
            time.sleep(self.sleep_time)

    def run(self):
        count = 0
        w1 = self.work1()
        w2 = self.work2()
        while True:
            next(w1)
            next(w2)

            if count > MAX_COUT:
                print("count get max: {}, then break".format(MAX_COUT))
                break
            else:
                count += 1


class GeventCoroutine(object):
    def __init__(self):
        self.sleep_time = 3

    def func_test(self, coroutine_name):
        for i in range(5):
            print(coroutine_name, i, datetime.now())
            time.sleep(self.sleep_time)

    def run(self):
        monkey.patch_all()   # 将耗时的操作, 使用gevent
        gevent.joinall([
            gevent.spawn(self.func_test, "work1"),
            gevent.spawn(self.func_test, "work2")
        ])


if __name__ == '__main__':
    # test1 = YieldCoroutine()
    # test1.run()

    test2 = GeventCoroutine()
    test2.run()