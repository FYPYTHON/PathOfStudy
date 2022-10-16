#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/15 22:47
# @Author  : 1823218990@qq.com
# @File    : common_msg
# @Software: Pycharm
import json

SOCKET_CONNECT = {'request': 'connect'}
SOCKET_CONNECT_RESPONSE = {'response': 'connect'}

PLAYERS_SEAT = {
    'play1': False,
    'play2': False,
    'play3': False,
    'play4': False
}

PACKET_REQUEST = {
    'request': '',
    'time': '',
    'uuid': '',
    'role': '',
    'table': '',
    'data': {}
}
PACKET_RESPONSE = {
    'response': '',
    'time': '',
    'uuid': '',
    'table': '',
    'role': '',
    'data': {}
}


def json_dumps(msg):
    try:
        data = json.dumps(msg).encode('utf-8')
    except:
        data = '{}'
    return data


def json_loads(msg):
    try:
        data = json.loads(msg.decode('utf-8'))
    except:
        data = {}
    return data


def check_seat(seat_single):
    count = 0
    for role, status in seat_single.items():
        if status is True:
            count += 1
    return count