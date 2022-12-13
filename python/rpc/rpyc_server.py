#!python3
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


class RpycServer(Service):
    NO_ERROR = 0
    HAS_ERROR = 1

    def __init__(self):
        pass

    def subcommand(self, cmd, timeout=10):
        child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        timer = Timer(timeout, lambda process: process.kill(), [child])
        try:
            timer.start()
            stdout, stderr = child.communicate()
            return_code = child.returncode
            if 0 != return_code:
                print("cmd:%s.error code is %d, output is %s" % (cmd, return_code, stderr.decode('utf-8')), end="\n")
                return return_code, stderr.decode('utf-8')
            else:
                print(stdout.decode('utf-8'), end="\n")
                return return_code, stdout.decode('utf-8')
        except Exception as e:
            print(e)
        # finally:
            timer.cancel()
            return -1, "error"

    def on_connect(self, conn):
        print("on_connect: {}".format(conn))

    def on_disconnect(self, conn):
        print("on_disconnect: {}".format(conn))

    def exposed_status(self):
        return self.NO_ERROR, 'ok'

    def exposed_cmd(self, cmd, timeout=10):
        code, msg = self.subcommand(cmd, timeout=timeout)
        return code, msg


if __name__ == '__main__':
    rpyc_s = ThreadPoolServer(RpycServer, port=9251)
    rpyc_s.start()
