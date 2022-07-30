#!/usr/bin/python3
# 2 核 2 cpu
"""
single 0.08220267295837402
thread 0.034249305725097656
"""

import threading
import time
NUMS = 2


def function_to_run():
    import urllib.request
    for i in range(10):
        with urllib.request.urlopen("http://127.0.0.1:8085/cbs") as f:
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
  




