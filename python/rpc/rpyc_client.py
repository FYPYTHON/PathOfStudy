#!python3
# coding=utf-8


import os
import sys
cur_file = os.path.realpath(sys.argv[0])
cur_path = os.path.dirname(cur_file)

print(cur_path)

sys.path.append(os.path.join(cur_path, "lib"))
import rpyc


class RpycClient(object):
    def __init__(self, host="127.0.0.1", port=9251):
        self.rpyc_client = rpyc.connect(host=host, port=port)

    def cmd(self, str_cmd):
        if str_cmd == "":
            code, data = self.rpyc_client.root.cmd("hostname && ps -ef | grep supervisord")
        else:
            code, data = self.rpyc_client.root.cmd(str_cmd)
        print("return:", code, "\n content:\n", data, end="\n")


if __name__ == '__main__':
    client = RpycClient()
    print(client.rpyc_client.root)
    client.cmd("")