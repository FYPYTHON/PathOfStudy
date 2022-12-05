# coding=utf-8
import logging
import threading
import time
import random
"""
如果信号量的计数器等于0，则阻塞这个信号量的acquire()方法，直到得到另一个不同线程的通知。
如果信号量的计数器大于0，则将这个值递减。生产者创建一个元素时，他会释放信号量，然后消费者得到信号量，并消费共享的资源。

    信号量的一个特俗用法死互斥锁（mutex）。互斥锁就是内部变量初始化为1的一个信号量，
可以实现对数据和资源的互斥访问。
    信号量的两个问题：
    * 无法避免一个线程在同一个信号量上完成多个等待操作。相对于所完成的等待操作，
      很容易忘记完成所有必要的释放操作（释放操作数要与等待操作数相同）。
    * 可能遇到死锁的情况。例如，t1线程在s1信号量上执行一个等待，t2线程在s2信号量上
      执行一个等待，然后t1在s2上执行等待，而t2在s1上执行一个等待，这就会产生一个死锁。
"""

LOG_FORMAT = "%(levelname)-8s %(asctime)s %(threadName)-17s %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

semaphore = threading.Semaphore()
item = 0


def consumer():
    logging.info("Consumer is waiting.")
    semaphore.acquire()
    logging.info("Consumer notify: item number {}".format(item))


def producer():
    global item
    time.sleep(3)
    item = random.randint(0, 100)
    logging.info("Producer notify: item number {}".format(item))
    semaphore.release()


# Main Program
def main():
    for i in range(10):
        t1 = threading.Thread(target=consumer)
        t2 = threading.Thread(target=producer)

        t1.start()
        t2.start()

        t1.join()
        t2.join()


if __name__ == "__main__":
    main()
