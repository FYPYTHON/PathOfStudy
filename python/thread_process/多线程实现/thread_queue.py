#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/23 9:32
# @Author  : 1823218990@qq.com
# @File    : thread_queue
# @Software: Pycharm

"""
queue模块最佳实践，使多线程编程更为安全。因为他会有效的将一个资源的所有访问排队，
实现一种更简洁、更可读的设计模式。

put(): 队列中放入一个元素
get(): 从队列中删除并返回一个元素
task_done(): 每次处理一个元素时需要调用这个方法。
join(): 阻塞，直到所有元素都已经处理。
"""
from threading import Thread
from queue import Queue
import time
import random


class Producer(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self) -> None:
        for i in range(5):
            item = random.randint(0, 256)
            self.queue.put(item)

            print("Producer notify: item N {} appended to queue by {}".format(item, self.name))
            time.sleep(1)


class Consumer(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self) -> None:
        while True:
            item = self.queue.get()
            print("Consumer notify: item N {} popped from queue by {}".format(item, self.name))
            self.queue.task_done()


if __name__ == '__main__':
    queue = Queue()
    t1 = Producer(queue)
    t2 = Consumer(queue)
    t3 = Consumer(queue)
    t4 = Consumer(queue)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
