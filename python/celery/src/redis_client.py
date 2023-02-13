#!/opt/midware/python3.8/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/12/20 20:36
# @Author  : 1823218990@qq.com
# @File    : redis_client.py
# @Software: Pycharm
import sys
import os
cur_path = os.path.dirname(os.path.realpath(sys.argv[0]))
CELERY_DIR = os.path.dirname(cur_path)

# print(CELERY_DIR)
sys.path.insert(0, CELERY_DIR)
sys.path.insert(1, os.path.join(CELERY_DIR, 'lib/python3.8/site-packages'))

print(sys.path)

from src.config import redis_host, redis_password, redis_port
import redis
# 默认redis入库编码是utf-8，如果要修改的话，需要指明 charset 和 decode_responsers 为True
# r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWORD,
#                       socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict',
#                       decode_responses=False, unix_socket_path=None)

REDIS_TYPE_MAP = {
    "set": b"set"
}

pool = redis.ConnectionPool(host=redis_host, password=redis_password, port=redis_port, db=0)
r = redis.StrictRedis(connection_pool=pool)
pipe = r.pipeline()
keys = r.keys()
print("keys:", keys)

# for key in keys:
#     print(f"{key} ({pipe.type(key)}) : {pipe.get(key)} \n")


def delete_data(r, key, data):
    try:
        # json_data = eval(data)
        r.delete(key)
        print("delete:", key)
    except Exception as e:
        print("error:", e)
        pass


def redisdata2json(str_data):
    if not isinstance(str_data, str):
        return None
    import json
    # print("ori:", str_data)
    json_data = json.loads(str_data)
    # task_id = json_data.get("task_id")
    date_done = json_data.get("date_done")
    # print("date:", date_done)
    fmt_date = iso2datetime(date_done)
    # print("fmt date:", fmt_date)
    json_data.setdefault("date_done", fmt_date)
    print(f"{json_data} \n")


def iso2datetime(tt, fmt="%Y-%m-%dT%H:%M:%S.%f"):
    try:
        from datetime import datetime
        fmt_tt = datetime.strptime(tt, fmt)
        # print("fmt_tt:", fmt_tt, tt, fmt)
        return fmt_tt
    except Exception as e:
        print(e)
        return None


print(f"------len(keys): {len(keys)}-------\n")
for key in keys:
    try:
        str_key = key.decode('utf-8')
        if "_kombu.binding.celery" in str_key:
            print(r.type(str_key))
            if r.type(str_key) == b'set':
                rset = r.smembers(str_key)
                print("redis set:", rset)
            continue
        if not key.startswith(b"celery-task-meta"):
            continue
        data = r.get(str_key)
        str_data = data.decode('utf-8')
        # print(str_key, ":", data, ":")
        redisdata2json(str_data)
        # if len(keys) > 5:
        #     delete_data(r, key, str_data)
    except Exception as e:
        print("error:", key, ":", e)


pipe.close()
pool.disconnect()
r.close()
