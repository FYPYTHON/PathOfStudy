# coding=utf-8
import sys
sys.path.append("/opt/midware/FSTornado/python3_fs/lib/python3.5/site-packages")
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.escape
import tornado.options
import logging.config
from tornado.log import app_log as weblog
import warnings
import json

warnings.filterwarnings("ignore")
from tornado.options import define, options

define("port", default=9081, help="run on the given port", type=int)


class Indexhandler(tornado.web.RequestHandler):
    def get(self):
        print("pid: ", os.getpid(), os.getppid())
        return self.write(json.dumps({"error_code": 1, "msg": "go"}))


if __name__ == "__main__":
    try:
        import setproctitle
        setproctitle.setproctitle("test_app")     # set process name in linux environment
    except:
        pass

    # tornado.options.parse_command_line()
    app = tornado.web.Application([(r'/', Indexhandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(9081)
    # http_server.bind(options.port)
    try:
        http_server.start(0)    # linux use mutli process
    except:
        print("window app start...")
        pass

    tornado.ioloop.IOLoop.current().start()



