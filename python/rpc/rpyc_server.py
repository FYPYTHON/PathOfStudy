#!python3
"""
使用装饰器(@rpyc.service, @rpyc.exposed), 可以直接使用不带exposed_前缀 ???
"""
import os
import sys
cur_file = os.path.realpath(sys.argv[0])
cur_path = os.path.dirname(cur_file)

print(cur_path)

sys.path.append(os.path.join(cur_path, "lib"))
import subprocess
from threading import Timer
import rpyc
from rpyc import Service
from rpyc.utils.server import ThreadedServer, ThreadPoolServer


# logger
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("./server.log")
fmt = logging.Formatter('[%(levelname)s]%(asctime)s %(filename)10s[%(lineno)s]- %(message)s')
console_handler.setFormatter(fmt)
file_handler.setFormatter(fmt)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.info("client start ...")
# logger


class RpycServer(Service):
    NO_ERROR = 0
    HAS_ERROR = 1

    def __init__(self):
        self.logger = logger

    def subcommand(self, cmd, timeout=10):
        """
        print("cmd:%s.error code is %d, output is %s" % (cmd, return_code, stderr.decode('utf-8')), end="\n")
        :param cmd:
        :param timeout:
        :return:
        """
        child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        timer = Timer(timeout, lambda process: process.kill(), [child])
        try:
            timer.start()
            stdout, stderr = child.communicate()
            return_code = child.returncode
            if 0 != return_code:
                self.logger.info("cmd:%s.error code is %d, output is %s" % (cmd, return_code, stderr.decode('utf-8')))
                return return_code, stderr.decode('utf-8')
            else:
                self.logger.error(stdout.decode('utf-8'))
                return return_code, stdout.decode('utf-8')
        except Exception as e:
            self.logger.error(e)
        # finally:
            timer.cancel()
            return -1, "error"

    def on_connect(self, conn):
        self.logger.info("on_connect: {}".format(conn))

    def on_disconnect(self, conn):
        self.logger.info("on_disconnect: {}".format(conn))

    def exposed_status(self):
        return self.NO_ERROR, 'ok'

    def exposed_hostname(self):
        cmd = "hostname"
        code, msg = self.subcommand(cmd)
        if code == 0:
            return msg
        else:
            return ""

    def exposed_cmd(self, cmd, timeout=10):
        code, msg = self.subcommand(cmd, timeout=timeout)
        return code, msg


if __name__ == '__main__':
    rpyc_s = ThreadPoolServer(RpycServer, port=9251)
    rpyc_s.start()
