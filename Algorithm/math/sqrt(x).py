# coding=utf-8
from math import fabs

PRECISION = 1e-8
number = 7

cc = 1


def myPow(x, n):
    if int(n) == 0:
        return 1
    else:
        global cc
        cc += 1
        tmp = myPow(x, n/2)
        tmp *= tmp
        if n % 2:
            if n > 0:
                tmp *= x
            else:
                tmp /= x
        return tmp


def mySqrt(x):
    res = x
    count = 1
    while fabs(res * res - x) > PRECISION:
        res = res / 2 + x / (2 * res)
        count += 1
    return res, count


def twoSplit(x):

    sta = 0
    end = x
    mid = (sta + end) / 2
    count = 1
    while fabs(mid ** 2 - x) > PRECISION:
        if mid ** 2 > x:
            end = mid
        else:
            sta = mid
        mid = (sta + end) / 2
        count += 1
    return mid, count


# print(mySqrt(number))
# print(twoSplit(number))

print(myPow(2, 5), cc)