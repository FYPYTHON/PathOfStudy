#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/15 22:26
# @Author  : 1823218990@qq.com
# @File    : gcpd_client
# @Software: Pycharm

import os
import time
from datetime import datetime
import socket
import logging
import logging.config

# ------ local
import sys
sys.path.append("E:\worksapce\python\GCPDCardGame")
import common_msg

class GCPDClient(object):
    def __init__(self, local_ip='127.0.0.1', local_port=26124, loglevel="INFO", role='player1', table='0'):
        self._ip = local_ip
        self._port = local_port
        self._loglevel = loglevel
        self._ngix_port = 24191
        self._concurrency = 500
        self.gcpd_socket = None
        self.logger = None

        self.gspd_nodes = dict()

        # 初始化日志
        self.init_log()
        # 初始化服务socket
        self.init_socket()
        # 初始化role
        self._role = role
        self._table = table


    def init_log(self):
        logpath = "/opt/log/gcpd"
        logConfig = {

            'version': 1,
            'loggers': {
                'gcpd_c': {
                    'level': '{}'.format(self._loglevel),
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
                    'level': '{}'.format(self._loglevel),
                    'formatter': 'timedRotating',
                    'filename': '{}/client.log'.format(logpath),
                    'backupCount': 2,
                    'maxBytes': 50 * 1024 * 1024,  # 文件最大50M
                    'encoding': 'utf-8'
                },
            }
        }
        if not os.path.exists(logpath):
            os.makedirs(logpath)
        logging.config.dictConfig(logConfig)
        self.logger = logging.getLogger("gcpd_c")

    def init_socket(self):
        try:
            self.gcpd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.gcpd_socket.settimeout(1)
            self.gcpd_socket.connect((self._ip, self._port))
            self.logger.info("{} connect {}:{} ok".format(self.gcpd_socket, self._ip, self._port))
            self.send_msg(common_msg.json_dumps(common_msg.SOCKET_CONNECT))
        except Exception as e:
            self.logger.error("{}".format(e))
            self.gcpd_socket = None

    def update_nodes(self, _socket):
        pass

    def send_msg(self, msg):
        self.gcpd_socket.send(msg)
        self.logger.debug("send msg:{}".format(msg))

    def process_msg(self, msg):
        msg = common_msg.json_loads(msg)
        self.logger.debug("receive msg:{}".format(msg))
        if msg.get("response", "") == "connect":
            self.logger.debug("receive connect from server")
            request_msg = common_msg.PACKET_REQUEST.copy()
            request_msg['request'] = 'getseat'
            request_msg['role'] = self._role
            request_msg['table'] = self._table
            request_msg['time'] = time.time()
            self.send_msg(common_msg.json_dumps(request_msg))
        elif msg.get('response', "") == "getseat":
            rep_data = msg.get('data', {})
            request_msg = common_msg.PACKET_REQUEST.copy()
            if not rep_data.get(self._role, False):
                self.logger.debug("role: {} is {}:".format(self._role, rep_data.get(self._role)))
                request_msg['request'] = 'seat'
            else:
                self.logger.error("table :{} role: {} is not empty".format(self._table, self._role))
                request_msg['request'] = 'getseat'

            request_msg['role'] = self._role
            request_msg['table'] = self._table
            request_msg['time'] = time.time()
            self.send_msg(common_msg.json_dumps(request_msg))
        elif msg.get('response', "") == 'seat':
            rep_data = msg.get('data', {})
            # 座位已选, 等待开始
            if common_msg.check_seat(rep_data) == 4:
                self.logger.info(" 4 role, then start...")
            else:
                self.logger.info("not 4 role, then wait...")
                request_msg = common_msg.PACKET_REQUEST.copy()
                request_msg['request'] = 'seat'
                request_msg['role'] = self._role
                request_msg['table'] = self._table
                request_msg['time'] = time.time()
                self.send_msg(common_msg.json_dumps(request_msg))

        elif msg.get("response", "") == "pong":
            time.sleep(2)
            self.logger.debug("receive pong from server")
            request_msg = common_msg.PACKET_REQUEST.copy()
            request_msg['request'] = 'ping'
            request_msg['time'] = time.time()
            self.send_msg(common_msg.json_dumps(request_msg))

    def run(self):
        while True:
            print('--', datetime.now(), self.gcpd_socket)
            if self.gcpd_socket is None:
                self.init_socket()
                time.sleep(2)
            try:
                msg = self.gcpd_socket.recv(1024)
                self.process_msg(msg)
            except Exception as e:
                self.logger.debug("{}".format(e))
                self.gcpd_socket = None


if __name__ == '__main__':

    # gspd.run()
    from multiprocessing import Process
    from threading import Thread
    role = 'player2'
    gspd = GCPDClient(loglevel='DEBUG', role=role)
    Thread(target=gspd.run).start()

