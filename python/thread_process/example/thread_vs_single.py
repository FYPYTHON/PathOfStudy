#!/usr/bin/python3
# 2 核 2 cpu
"""
ok
ok
single 4.051486015319824
ok
ok
thread 1.9088609218597412
"""

import threading
import time
NUMS = 2


def function_to_run():
    fh=open("test.dat","rb")
    size = 1024
    for i in range(1000):
        # fh=open("testTimeout.py","rb")
        dd = fh.read(size)
        if dd == "":
            fh.seek(0)
        # fh.close()
        time.sleep(0.001)
    print("ok")
    fh.close()


def function_to_run1():
    import urllib.request
    for i in range(10):
        with urllib.request.urlopen("https://www.baidu.com/")as f:
            f.read(1024)

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
  




