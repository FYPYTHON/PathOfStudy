#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/12 10:39
# @Author  : 1823218990@qq.com
# @File    : thread_with
# @Software: Pycharm
"""
with语法：
https://www.kawabangga.com/posts/2010
"""
import threading
import logging
logging.basicConfig(level=logging.DEBUG, format="(%(threadName)-10s) %(message)s")


def threading_with(statement):
    with statement:
        logging.debug("%s acquire via with" % statement)


def threading_not_with(statement):
    statement.acquire()
    try:
        logging.debug("%s acquire directly" % statement)
    except Exception as e:
        print(e)
    finally:
        statement.release()


if __name__ == '__main__':
    lock = threading.Lock()
    rlock = threading.RLock()
    condition = threading.Condition()
    semaphore = threading.Semaphore(1)
    threadlists = [lock, rlock, condition, semaphore]
    t_list = []
    for stm in threadlists:
        t1 = threading.Thread(target=threading_with, args=(stm,))
        t2 = threading.Thread(target=threading_not_with, args=(stm,))
        t1.start()
        t2.start()
        t_list.append(t1)
        t_list.append(t2)

    for t in t_list:
        t.join()
