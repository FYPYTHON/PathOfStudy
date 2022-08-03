# coding=utf-8
from amqplib import client_0_8 as amqp
HOST = '172.16.83.226'
USER = 'root'
PAWD = 'feiying'

#
HOST = '10.67.18.100:5872'
USER = 'dev'
PAWD = 'dev'


def main():
    server = {'host': HOST, 'userid': USER, 'password': PAWD, 'ssl': False}
    x_name = 'ops.collector.ex'
    routing_key = "ops.mt.k"
    conn = amqp.Connection(server['host'],
                           userid=server['userid'],
                           password=server['password'],
                           ssl=server['ssl']
                           )
    ch = conn.channel()
    ch.access_request('/data', active=True, write=True)
    ch.exchange_declare(exchange=x_name, type='topic', durable=True, auto_delete=False)
    retry = True
    import time
    headers = {"timestamp_in_ms": int(time.time()), "platformid": "mooooooo-oooo-oooo-oooo-defaultplatf"}
    count = 0
    while retry:
        msg_body = input('>')
        # msg_body = str(time.time())
        count += 1
        msg_body = str(count) + "," + str(time.time()) + "."
        msg = amqp.Message(msg_body, content_encoding='UTF-8', application_headers=headers)
        msg.properties['delivery_mode'] = 2
        ch.basic_publish(msg, x_name, routing_key)

        # if msg_body == 'quit':
        #     retry = False
        print(count)
        if count == 200:
            break

    ch.close()
    conn.close()


if __name__ == '__main__':
    main()