# coding=utf-8
import logging
import threading
import time
import random
"""
event对象管理一个内部标志，可以用clear()设置为false，用set设置为true。is_set()测试。
线程用wait()方法等待一个信号，用set()方法发送信号。

t1线程向列表追加一个值，然后设置事件来通知消费之。
消费者的wait()调用停止阻塞，从列表获取这个整数。
"""

LOG_FORMAT = "%(levelname)-8s %(asctime)s %(threadName)-17s %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

items = []
event = threading.Event()


class Consumer(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)

    def run(self):
        while True:
            time.sleep(2)
            event.wait()
            item = items.pop()
            logging.info("Consumer notify:{} popped by 1 item : {}".format(item, self.name))


class Producer(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Producer, self).__init__(*args, **kwargs)

    def run(self):
        for i in range(5):
            time.sleep(2)
            item = random.randint(0, 100)
            items.append(item)
            logging.info("Producer notify: item {} appended by {}".format(item, self.name))
            event.set()
            event.clear()


if __name__ == '__main__':
    t1 = Producer()
    t2 = Consumer()

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == '__main__':
    t1 = Producer()
    t2 = Consumer()

    t1.start()
    t2.start()

    t1.join()
    t2.join()
