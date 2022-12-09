#!python3
# coding=utf-8


import os
import sys
cur_file = os.path.realpath(sys.argv[0])
cur_path = os.path.dirname(cur_file)

print(cur_path)

sys.path.append(os.path.join(cur_path, "lib"))
import rpyc


class RpycClient():
    def __init__(self, host="127.0.0.1", port=9251):
        self.rpyc_client = rpyc.connect(host=host, port=port)

    def cmd(self):
        data = self.rpyc_client.cmd("ps -ef | grep supervisord")
        print(data)
