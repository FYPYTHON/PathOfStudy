#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/12 11:23
# @Author  : 1823218990@qq.com
# @File    : thread_performance
# @Software: Pycharm
"""
functinon pass:
Starting tests
non_threaded (1 iters)  0.000001 seconds
threaded (1 threads)    0.000110 seconds
Iterations complete
non_threaded (2 iters)  0.000002 seconds
threaded (2 threads)    0.000213 seconds
Iterations complete
non_threaded (4 iters)  0.000002 seconds
threaded (4 threads)    0.000372 seconds
Iterations complete
non_threaded (8 iters)  0.000005 seconds
threaded (8 threads)    0.000741 seconds
Iterations complete
"""
"""
function:
    a, b = 0, 1
    for i in range(10000):
        a, b = b, a + b
Starting tests
non_threaded (1 iters)  0.002149 seconds
threaded (1 threads)    0.002347 seconds
Iterations complete
non_threaded (2 iters)  0.004427 seconds
threaded (2 threads)    0.004963 seconds
Iterations complete
non_threaded (4 iters)  0.009055 seconds
threaded (4 threads)    0.009981 seconds
Iterations complete
non_threaded (8 iters)  0.020102 seconds
threaded (8 threads)    0.021710 seconds
Iterations complete

------------


Process finished with exit code 0

"""

from threading import Thread


class threads_object(Thread):
    def run(self):
        function_to_run()


class nothreads_object(object):
    def run(self):
        function_to_run()


def non_threaded(num_iter):
    funcs = []
    for i in range(int(num_iter)):
        funcs.append(nothreads_object())
    for i in funcs:
        i.run()


def threaded(num_threads):
    funcs = []
    for i in range(int(num_threads)):
        funcs.append(threads_object())
    for i in funcs:
        i.start()
    for i in funcs:
        i.join()


# def function_to_run():
#     fh = open("E:\\mountdisk.sh", "rb")
#     size = 4096
#     for i in range(10000):
#         fh.read(size)
def function_to_run():
    import urllib.request
    for i in range(10):
        with urllib.request.urlopen("https://www.baidu.com/")as f:
            f.read(1024)


def show_results(func_name, results):
    print("%-23s %4.6f seconds" % (func_name, results))


def main1():
    import sys
    from timeit import Timer
    repeat = 100
    number = 1
    num_threads = [1, 2, 4, 8]
    print('Starting tests')
    for i in num_threads:
        t = Timer("non_threaded(%s)" % i, "from __main__ import non_threaded")
        best_result = min(t.repeat(repeat=repeat, number=number))
        show_results("non_threaded (%s iters)" % i, best_result)
        t = Timer("threaded(%s)" % i, "from __main__ import threaded")
        best_result = min(t.repeat(repeat=repeat, number=number))
        show_results("threaded (%s threads)" % i, best_result)
        print('Iterations complete')

if __name__ == "__main__":
    main1()
    print("\n------------\n")
