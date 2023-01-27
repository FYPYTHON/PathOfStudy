#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/15 21:50
# @Author  : 1823218990@qq.com
# @File    : gcpd_server
# @Software: Pycharm
import os
from datetime import datetime
import socket
import socketserver

import logging
import logging.config
from threading import Thread

# ------ local
import common_msg


class GCPDServer(object):
    def __init__(self, local_ip='0.0.0.0', local_port=26124, loglevel="INFO"):
        self._ip = local_ip
        self._port = local_port
        self._loglevel = loglevel
        self._ngix_port = 24191
        self._concurrency = 500
        self.gcpd_socket = None
        self.card_tables = dict()
        self._max_tables = 2
        self.logger = None

        self.gspd_nodes = dict()

        # 初始化日志
        self.init_log()
        # 初始化服务socket
        self.init_socket()
        # 初始化card table
        self.init_card_tables()

    def init_log(self):
        logpath = "/opt/log/gcpd"
        logConfig = {

            'version': 1,
            'loggers': {
                'gcpd_s': {
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
        self.logger = logging.getLogger("gcpd_s")

    def init_socket(self):
        try:
            self.gcpd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.gcpd_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.gcpd_socket.bind((self._ip, self._port))
            self.gcpd_socket.listen(self._concurrency)   # n表示socket的 '排队个数', 即超过n后面的连接需要排队. 不是只能有n个连接.
            self.logger.info("{} init ok".format(self.gcpd_socket))
        except Exception as e:
            self.logger.error("{}".format(e))
            self.gcpd_socket = None

    def init_card_tables(self):
        for i in range(self._max_tables):
            self.card_tables[str(i)] = common_msg.PLAYERS_SEAT.copy()

    def update_nodes(self, _socket):
        pass

    def process_client(self, client_socket, client_addr):
        while True:
            msg = client_socket.recv(1024)
            # self.logger.debug(msg)
            msg = common_msg.json_loads(msg)
            self.logger.debug("receive msg {} {}".format(client_addr, msg))
            table = msg.get('table', None)
            role = msg.get('role', None)
            data = msg.get('data', None)

            if msg.get("request", "") == "connect":
                rep_msg = common_msg.json_dumps(common_msg.SOCKET_CONNECT_RESPONSE)
                client_socket.send(rep_msg)
            elif msg.get("request", "") == "ping":
                rep_msg = common_msg.PACKET_RESPONSE.copy()
                rep_msg['response'] = 'pong'
                client_socket.send(common_msg.json_dumps(rep_msg))
            elif msg.get("request", '') == "getseat":
                rep_msg = common_msg.PACKET_RESPONSE.copy()
                rep_msg['response'] = 'getseat'
                rep_msg['data'] = self.card_tables.get(table, {})
                client_socket.send(common_msg.json_dumps(rep_msg))
            elif msg.get('request', '') == 'seat':
                if table not in self.card_tables.keys():
                    rep_msg = common_msg.PACKET_RESPONSE.copy()
                    rep_msg['response'] = 'getseat'
                    rep_msg['table'] = table
                    rep_msg['role'] = role
                    rep_msg['data'] = self.card_tables.get(rep_msg['table'], {})
                    client_socket.send(common_msg.json_dumps(rep_msg))
                else:
                    self.card_tables[table][role] = True
                    rep_msg = common_msg.PACKET_RESPONSE.copy()
                    rep_msg['response'] = 'seat'
                    rep_msg['table'] = table
                    rep_msg['role'] = role
                    rep_msg['data'] = self.card_tables.get(rep_msg['table'], {})
                    client_socket.send(common_msg.json_dumps(rep_msg))
            else:
                rep_msg = b'{}'
            self.logger.debug("send msg {}".format(rep_msg))

    def run(self):
        while True:
            print('--', datetime.now())
            try:
                client_socket, client_addr = self.gcpd_socket.accept()

                if client_addr not in self.gspd_nodes.keys():
                    self.gspd_nodes[client_addr] = dict()
                    self.gspd_nodes[client_addr]['socket'] = client_socket

                self.logger.debug("accept client_socket:{}, client_addr:{}".format(client_socket, client_addr))
                # self.process_client(client_socket, client_addr)
                Thread(target=self.process_client, args=(client_socket, client_addr)).start()
            except Exception as e:
                self.logger.debug("{}".format(e))


if __name__ == '__main__':
    gspd = GCPDServer(loglevel='DEBUG')
    gspd.run()