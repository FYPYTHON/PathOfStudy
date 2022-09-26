# coding=utf-8
"""
python3.5 code runtime is 4.455146769061685
python3.6 code runtime is 4.475854706950486
python3.7 code runtime is 3.4917389350011945
python3.8 code runtime is 4.390280680265278
python3.11 code runtime is 1.1779353017918766
"""


import time

def timer(func):
    def inner():
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        print('code runtime is {}'.format(end-start))

    return inner

@timer
def range_tracker():
    lst = []
    for i in range(10000000):
        lst.append(i**2)

range_tracker()

