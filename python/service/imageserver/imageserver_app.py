# coding=utf-8
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.escape
from settings import urls
import tornado.options
import logging.config
from tornado.log import app_log as weblog
from settings.logConfig import logConfig
import warnings

warnings.filterwarnings("ignore")
from tornado.options import define, options

define("port", default=9081, help="run on the given port", type=int)
logging.config.dictConfig(logConfig)
MAX_STREAMED_SIZE = 1024 * 1024 * 1024


def check_path_exist():
    if not os.path.exists("/opt/data/fs"):
        os.makedirs('/opt/data/fs')


class Application(tornado.web.Application):
    def __init__(self):

        settings = dict(
            template_path=(os.path.join(os.path.dirname(__file__), "templates")),
            static_path=(os.path.join(os.path.dirname(__file__), "static")),
            cookie_secret="f6d4f6de102f29b5cd37cd5eQtsdfsfdsdJ5/xJ89E=",
            session_secret="12f29b5c61c118ccd37cd5eQtsdfsfdsdJ5/xJ89E=",
            session_timeout=300,   # seconds
            token_timeout=10,   # minutes
            top_path="/opt/data/fs",
            login_url="/login",
            debug=True,
            autoescape=None,
            xheaders=True,
            # xsrf_cookies=True,
        )

        handlers = urls.url
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    try:
        import setproctitle
        setproctitle.setproctitle("imageserver")     # set process name in linux environment
    except:
        pass
    check_path_exist()
    # tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app, max_buffer_size=4 * MAX_STREAMED_SIZE)
    http_server.listen(options.port)
    try:
        http_server.start(2)    # linux use mutli process
    except:
        print("window app start...port={}".format(options.port))
        pass
    weblog.info("-- imageserver start .... pid:{} ".format(os.getpid()))
    tornado.ioloop.IOLoop.instance().start()



