#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/19 22:24
# @Author  : 1823218990@qq.com
# @File    : thread_gcpd_server.py
# @Software: Pycharm

import socketserver
import time

# 
import common_msg
from common_log import logger
from threading import Timer


class GcpdServer(socketserver.StreamRequestHandler):
    nodes = []
    nodes_connect = dict()
    max_tables = 100
    card_tables = None
    timeout = 1

    @classmethod
    def heart_beat(self):
        if self.card_tables is None:
            self.card_tables = dict()
            for i in range(self.max_tables):
                self.card_tables[str(i)] = common_msg.PLAYERS_SEAT.copy()

        logger.debug(self.nodes_connect)

        task = Timer(5, self.heart_beat)
        task.start()

    def process_msg(self, client_socket, client_addr):
        msg = client_socket.recv(1024)
        # logger.debug(msg)
        msg = common_msg.json_loads(msg)
        logger.debug("receive msg {} {}".format(client_addr, msg))
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
        logger.debug("send msg {}".format(rep_msg))
    
    def handle(self):

        # if self.card_tables is None:
        #     self.card_tables = dict()
        #     for i in range(self.max_tables):
        #         self.card_tables[str(i)] = common_msg.PLAYERS_SEAT.copy()
        while True:
            try:
                # 状态

                # 处理
                self.process_msg(self.request, self.client_address)

                print(self.request)
                # msg = self.rfile.readline().strip()
                print(self.client_address)
                if self.client_address not in self.nodes:
                    self.nodes.append(self.client_address)
                    self.nodes_connect[self.client_address] = self.request
                # print(self.nodes_connect)

                time.sleep(5)

                # self.wfile.write(b'{"response": "connect"}')
            except Exception as e:
                print(e)
                break
        self.request.close()
        self.nodes.remove(self.client_address)
        self.nodes_connect.pop(self.client_address)


class ThreadGcpdServer(object):
    def __init__(self, local_ip='0.0.0.0', local_port=26124, loglevel="INFO"):
        self._ip = local_ip
        self._port = local_port
        self._loglevel = loglevel
        self._ngix_port = 24191

    def run(self):
        GcpdServer.timeout = 1
        GcpdServer.heart_beat()
        server = socketserver.ThreadingTCPServer((self._ip, self._port), GcpdServer)
        server.serve_forever()


if __name__ == '__main__':
    s = ThreadGcpdServer()
    s.run()