#!python3
# coding=utf-8


import os
import sys
cur_file = os.path.realpath(sys.argv[0])
cur_path = os.path.dirname(cur_file)

print(cur_path)

sys.path.append(os.path.join(cur_path, "lib"))
import rpyc

# logger
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("./client.log")
fmt = logging.Formatter('[%(levelname)s]%(asctime)s %(filename)10s[%(lineno)s]- %(message)s')
console_handler.setFormatter(fmt)
file_handler.setFormatter(fmt)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.info("client start ...")
# logger


class RpycClient(object):
    NO_ERROR = 0
    HAS_ERROR = 1
    TIME_OUT = 10

    def __init__(self, host="127.0.0.1", port=9251):
        self.logger = logger
        self.logger.info("connect to {} {} ...".format(host, port))
        self.port = port
        self.rpyc_client = rpyc.connect(host=host, port=port)

    def cmd(self, str_cmd, result_list=None):
        """
        print("return: {}".format(code), end="\n")
        :param str_cmd:
        :param result_list:
        :return:
        """
        if result_list is None:
            result_list = []
        if str_cmd == "":
            code, data = self.rpyc_client.root.cmd("netstat -tnlp | grep {}".format(self.port))
        else:
            code, data = self.rpyc_client.root.cmd(str_cmd)
        result_list.append((str_cmd, code))
        self.logger.info("return: {}".format(code))
        self.logger.info("content: {}".format(data))

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
                # print("cmds result: {}".format(result_list))
                return self.HAS_ERROR
        self.logger.info("cmds result: {}".format(result_list))
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
    logger.info(client.rpyc_client.root)
    logger.info("remote status: {}".format(client.rpyc_client.root.status()))
    logger.info("remote hostname: {}".format(client.rpyc_client.root.hostname()))
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
