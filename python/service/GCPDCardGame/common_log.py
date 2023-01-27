#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/19 23:14
# @Author  : 1823218990@qq.com
# @File    : common_log
# @Software: Pycharm
import os
import logging
import logging.config
loglevel = 'DEBUG'

logpath = "/opt/log/gcpd"
logConfig = {

    'version': 1,
    'loggers': {
        'gcpd_s': {
            'level': '{}'.format(loglevel),
            'handlers': ['log', 'console'],
            'propagate': 'no'
        }
    },
    'formatters': {
        'timedRotating': {
            'format': '[%(levelname)s] %(asctime)s %(filename)15s [%(lineno)s] - %(message)s'
        }
    },
    'handlers': {
        'console': {
          'class': 'logging.StreamHandler',
          'level': 'DEBUG',
          'formatter': 'timedRotating',
          },
        'log': {
            'class': 'logging.handlers.RotatingFileHandler',  # size
            'level': '{}'.format(loglevel),
            'formatter': 'timedRotating',
            'filename': '{}/server.log'.format(logpath),
            'backupCount': 2,
            'maxBytes': 50 * 1024 * 1024,  # 文件最大50M
            'encoding': 'utf-8'
        },
    }
}
if not os.path.exists(logpath):
    os.makedirs(logpath)
logging.config.dictConfig(logConfig)
logger = logging.getLogger("gcpd_s")