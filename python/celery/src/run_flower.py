#!/opt/midware/python3.8/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/02/16 16:17
# @Author  : 1823218990@qq.com
# @File    : run_tasks.py
# @Software: Pycharm
"""
https://flower.readthedocs.io/en/latest/install.html
"""
from random import randint
import sys
import os


cur_path = os.path.dirname(os.path.realpath(sys.argv[0]))
CELERY_DIR = os.path.dirname(cur_path)

# print(CELERY_DIR)
lib_path = os.path.join(CELERY_DIR, 'lib/python3.8/site-packages')
sys.path.insert(0, CELERY_DIR)
sys.path.insert(1, lib_path)

# 2023 02 16
from src.mycelery import app

from datetime import datetime

from src.config import broker_url

import subprocess

cmd = [
    '{}/bin/flower'.format(CELERY_DIR),
    '--broker={}'.format(broker_url),      # 监控的broker的地址
    '--basic_auth=flower:fw123456',        # 登录flower需要的用户名和密码
    '--port=8088',                         # flower需要的端口号
    '--url_prefix=flower'                  # 主页的路径前缀 比如:https://west.com/flower/

]
if __name__ == '__main__':
    subprocess.run(cmd, env={"PYTHONPATH": "{}".format(lib_path)})

