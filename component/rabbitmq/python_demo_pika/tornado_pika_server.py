# coding=utf-8
import functools
import json
import tornado.web
import logging
log = logging.getLogger('mq')
# from handlers.notify import NotifyHandler
# from function.function import config
# from utils.utils import log

import pika
from pika.adapters import tornado_connection


HOST = '172.16.185.193`'
PORT = '6676'
USER = 'dev'
PAWD = 'KedaRmq!Dev_56'
MQ_QUEUE = 'text'
EXCHANGE = 'v1'
EXCHANGE_TYPE = 'topic'
ROUTING_KEY = 'example.text'
class PikaClient():
    def __init__(self, io_loop):
        self.io_loop = io_loop
        self.connected = False
        self.connecting = False
        self.connection = None
        self.channel = None
        self.message_count = 9

    def connect(self):
        if self.connecting:
            return
        self.connecting = True
        cred = pika.PlainCredentials(USER, PAWD)
        param = pika.ConnectionParameters(host=HOST, port=int(PORT), credentials=cred)
        self.connection = tornado_connection.TornadoConnection(param, custom_ioloop=self.io_loop,
                                                               on_open_callback=self.on_connected)
        self.connection.add_on_open_error_callback(self.err)
        self.connection.add_on_close_callback(self.on_closed)

    def err(self, conn):
        log.info('socket error', conn)
        pass

    def on_connected(self, conn):
        log.info('connected')
        self.connected = True
        self.connection = conn
        self.connection.channel(channel_number=1, on_open_callback=self.on_channel_open)

    def on_message(self, channel, method, properties, body):
        """
        channel: pika.Channel
        method: pika.spec.Basic.Deliver
        properties: pika.spec.BasicProperties
        body: bytes
        """
        log.info(body)
        print("channel :", channel)
        print("method :", method)
        print("properties :", properties)
        print('body : ', body)

    def on_channel_open(self, channel):
        self.channel = channel
        channel.basic_consume(on_message_callback=self.on_message, queue=MQ_QUEUE, auto_ack=True)
        return

    def on_closed(self, conn, c):
        log.info('pika close!')
        self.io_loop.stop()
        pass


class NotifyHandler(tornado.web.RequestHandler):

    def __init__(self, *argc, **argkw):
        self.status = 'not connected yet'
        self.message = ''
        self.channel = None
        super(NotifyHandler, self).__init__(*argc, **argkw)

    def open(self):
        self.status = "ws open"
        print(self.status)
        self.rabbit_connect()  # connect this websocket object to rabbitmq

    def rabbit_connect(self):
        self.application.pc.connection.channel(on_open_callback=self.rabbit_channel_in_ok)

    def rabbit_channel_in_ok(self, channel):
        print(channel)
        self.channel = channel

        cb = functools.partial(
            self.on_exchange_declareok, userdata=EXCHANGE)
        self.channel.exchange_declare(
            exchange=EXCHANGE,
            exchange_type=EXCHANGE_TYPE,
            callback=cb)
        #
        # print("NotifyHandler channel:", channel)
        # channel.queue_declare(MQ_QUEUE, exclusive=True, auto_delete=True, callback=self.on_queue_declareok)

    def on_exchange_declareok(self, _unused_frame, userdata):
        print("userdata:", userdata)
        self.channel.queue_declare(
            queue=MQ_QUEUE, callback=self.on_queue_declareok)

    def on_queue_declareok(self, _unused_frame):
        self.channel.queue_bind(
            MQ_QUEUE,
            EXCHANGE,
            routing_key=ROUTING_KEY,
            callback=self.on_bindok)

    def on_bindok(self, _unused_frame):
        # self.channel.basic_publish(EXCHANGE, ROUTING_KEY,
        #                             json.dumps(self.message, ensure_ascii=False),
        #                             properties)
        self.send_message(self.message)

    def send_message(self, message):
        hdrs = {u'مفتاح': u' قيمة', u'键': u'值', u'キー': u'値'}
        properties = pika.BasicProperties(
            app_id='example-publisher',
            content_type='application/json',
            headers=hdrs)
        self.channel.basic_publish(EXCHANGE, ROUTING_KEY,
                                    json.dumps(message, ensure_ascii=False),
                                    properties)

    def get(self):
        self.message = "ok..."
        self.open()
        import time
        return self.write(str(time.time()))

        pass


def main():
    port = 3002
    # is_debug = config('sys', 'debug')
    # print('DEBUG', is_debug)
    print('listen {}'.format(port))
    HANDLERS = [(r'/notify', NotifyHandler)]
    app = tornado.web.Application(
            HANDLERS,
            debug=True,
            )
    io_loop = tornado.ioloop.IOLoop.instance()
    app.pc = PikaClient(io_loop)
    app.pc.connect()
    http_server = tornado.httpserver.HTTPServer(app)
    app.listen(port)
    try:
        io_loop.start()
    except:
        io_loop.stop()


if __name__ == '__main__':
    main()