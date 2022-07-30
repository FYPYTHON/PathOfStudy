# coding=utf-8
import os
import time
from threading import Thread
from multiprocessing import Process


def func(num):
    for i in range(100):
        print(num, "->", "data:", i, "pid:", os.getpid(), "gpid:", os.getpgrp())
        time.sleep(10)


def func_new(num):
    t = Process(target=func, args=(str(i),))
    t.daemon = True
    t.start()
    t.join()


if __name__ == '__main__':
    print('current main pid is %s' % os.getpid())
    processes = []
    for i in range(3):
        # t = Process(target=func, args=(str(i),))
        t = Thread(target=func_new, args=(str(i),))
        t.daemon = True
        t.start()
        processes.append(t)
    try:
        for p in processes:
            p.join()
        # exit(-1)
    except Exception as e:
        print(e)