#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/19 10:26
# @Author  : 1823218990@qq.com
# @File    : fcntl
# @Software: Pycharm


def fcntl(fd, op, arg=0):
    return 0


def ioctl(fd, op, arg=0, mutable_flag=True):
    if mutable_flag:
        return 0
    else:
        return ""


def flock(fd, op):
    return


def lockf(fd, operation, length=0, start=0, whence=0):
    return
