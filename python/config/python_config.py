#!python3.9
# coding=utf-8
# 2023 10 26
"""
ini 文件解析
自定义注释符   保留注释
"""
import os
import sys

sys.path.append("/home/wgq/python/lib/python3.5/site-packages")
from configupdater import ConfigUpdater

delimiters = ('=',)
comment_prefixes = ('#', ';', "--")


def get_field_value(path, module, key):
    try:

        configer = ConfigUpdater(delimiters=delimiters, comment_prefixes=comment_prefixes, allow_no_value=True)
        configer.read(path, encoding="utf-8")
        data = configer.get(module, key).value
        return data
    except Exception as e:
        # print(repr(e))
        return None


def set_field_value(path, module, key, value):
    try:
        configer = ConfigUpdater(delimiters=delimiters, comment_prefixes=comment_prefixes, allow_no_value=True)
        configer.read(path, encoding="utf-8")
        configer.set(module, key, value)
        with open(path, "w") as fp:
            configer.write(fp)
    except Exception as e:
        print(repr(e))
        exit(-1)


if __name__ == '__main__':
    """
    python3.9 /home/wgq/python/python_config.py get_field_value /home/wgq/python/mpcadpcfg.ini DomainInfo  Domain0 12
    """
    if len(sys.argv) < 5:
        print("Wrong number of parameters:{} len:{}".format(sys.argv, len(sys.argv)))
        exit(-1)
    action = sys.argv[1]

    args = sys.argv[2:]
    # print(action, args)
    if action == "get_field_value":
        if len(args) != 3:
            print("get_field_value Wrong number of parameters:{} len:{}".format(args, len(args)))
            exit(-1)
        data = get_field_value(*args)
        print(data)
    elif action == "set_field_value":
        if len(args) != 4:
            print("set_field_value Wrong number of parameters:{} len:{}".format(args, len(args)))
            exit(-1)
        set_field_value(*args)
    else:
        print("function {} not found.".format(action))
