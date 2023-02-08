#!/opt/midware/python3.8/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/12/20 20:18
# @Author  : 1823218990@qq.com
# @File    : config.py
# @Software: Pycharm
"""

https://docs.celeryq.dev/en/stable/userguide/configuration.html

"""

from datetime import timedelta

nodes = "worker"

redis_host = "127.0.0.1"
redis_password = "fy123456"
redis_port = 6379
broker_url = f'redis://:{redis_password}@{redis_host}:{redis_port}/0'

# redis 中存储任务的状态和返回值
result_backend = f'redis://:{redis_password}@{redis_host}:{redis_port}/0'

broker_transport_options = {
    'visibility_timeout': 3600,  # 1 hour # 可见性超时时间定义了等待职程在消息分派到其他职程之前确认收到任务的秒数
    'fanout_prefix': True  # 设置一个传输选项来给消息加上前缀，这样消息只会被活动的虚拟主机收到

}


# 限制任务的速率，这样每分钟只允许处理 10 个该类型的任务
celery_annotations = {
    'tasks.cal_sum': {'rate_limit': '10/m'}
}

task_serializer = 'json'
# task_serializer
result_serializer = 'json'
accept_content=['json']
result_expires  = timedelta(minutes=30)  # 1小时
# celery_task_result_expires = 60 * 2


timezone = 'asia/shanghai'
enable_utc = False
# 该方式修改时区对延时任务不生效
# print(broker_url)


