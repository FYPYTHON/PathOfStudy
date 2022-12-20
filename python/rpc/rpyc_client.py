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
    NO_ERROR = 0
    HAS_ERROR = 1
    TIME_OUT = 10

    def __init__(self, host="127.0.0.1", port=9251):
        print("connect to {} {} ...".format(host, port))
        self.port = port
        self.rpyc_client = rpyc.connect(host=host, port=port)

    def cmd(self, str_cmd, result_list=None):
        if result_list is None:
            result_list = []
        if str_cmd == "":
            code, data = self.rpyc_client.root.cmd("netstat -tnlp | grep {}".format(self.port))
        else:
            code, data = self.rpyc_client.root.cmd(str_cmd)
        result_list.append((str_cmd, code))
        print("return: {}".format(code), end="\n")
        print("content: {}".format(data), end="\n")

    def cmds(self, clients, cmds):
        from multiprocessing import Manager, Process
        result_list = Manager().list()
        ps = []
        for i in range(len(cmds)):
            p = Process(target=clients[i].cmd, args=(cmds[i], result_list))
            ps.append(p)
        for p in ps:
            p.start()
        for p in ps:
            p.join(self.TIME_OUT)

        for res in result_list:
            cmd, code = res
            if code != self.NO_ERROR:
                # print("cmds result: {}".format(result_list), end="\n")
                return self.HAS_ERROR
        print("cmds result: {}".format(result_list), end="\n")
        return self.NO_ERROR


def threads_run(cmds):
    client = RpycClient(host=host)
    size = len(cmds)
    pool = ThreadPool(size)
    results = pool.map(client, cmds)
    pool.close()
    pool.join()
    
    
def main(host):
    client = RpycClient(host=host)
    print(client.rpyc_client.root)
    print("remote status: {}".format(client.rpyc_client.root.status()))
    print("remote hostname: {}".format(client.rpyc_client.root.hostname()))
    client.cmd("")

    cmds = ["ps -ef | grep firewalld | grep -v grep", "df ."]
    clients = []
    # client.cmds(cmds)
    for _ in cmds:
        temp_client = RpycClient(host=host)
        clients.append(temp_client)
    client.cmds(clients, cmds)


if __name__ == '__main__':
    argv = sys.argv
    if len(argv) == 2:
        host = argv[1]
    else:
        host = '127.0.0.1'
    main(host)
