#!/usr/bin/python3
# 234996720kb test.dat
"""
single 1.2693171501159668
thread 1.1729207038879395
"""

import threading
import time
NUMS = 2


def function_to_run():
    # fh = open("test.dat", "rb")
    for i in range(8):
        fh = open("test.dat", "rb")
        dd = fh.read()
        fh.close()


def no_thread():
    t1 = time.time()
    for i in range(NUMS):
        function_to_run()
    t2 = time.time()
    print("single", t2 - t1)


def with_thread():
    t1 = time.time()
    t_list = []
    for i in range(NUMS):
        t = threading.Thread(target=function_to_run)
        t.start()
        t_list.append(t)  
    for t in t_list:
        t.join()
    t2 = time.time()
    print("thread", t2 - t1)


if __name__ == "__main__":
    no_thread()
    with_thread()
  




