# coding=utf-8
import logging
import threading
import time
import random

LOG_FORMAT = "%(levelname)-8s %(asctime)s %(threadName)-17s %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

items = []
condition = threading.Condition()


class Consumer(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)

    def consume(self):
        with condition:
            if(len(items)) == 0:
                logging.info("no items to consume")
                condition.wait()
            item = items.pop()
            logging.info("consumed 1 item : {}".format(item))

            condition.notify()

    def run(self):
        for i in range(20):
            time.sleep(2)
            self.consume()


class Producer(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Producer, self).__init__(*args, **kwargs)

    def produce(self):
        with condition:
            if (len(items)) == 10:
                logging.info("items produced {} Stopped".format(len(items)))
                condition.wait()
            item = random.randint(0, 100)
            items.append(item)
            logging.info("produce 1 item : {}".format(item))

            condition.notify()

    def run(self):
        for i in range(20):
            time.sleep(2)
            self.produce()

if __name__ == '__main__':
    t1 = Producer()
    t2 = Consumer()

    t1.start()
    t2.start()

    t1.join()
    t2.join()
