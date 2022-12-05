# coding=utf-8
"""
重入锁（RLock）是一个同步原语，可以由同一个线程获得多次
同一个线程可以多次获得一个RLock锁。拥有重入锁的线程对应之前的每一个acquire（）调用都要做一个release（）调用，
在此之前，其他线程不能获得RLock锁

lock和RLock:
*锁在释放前只能获得一次，重入锁可以由同一个线程获得多次，而且必须释放同样的次数才能释放RLock.
*已得到的锁可以由任意的线程释放，而已得到的RLock只能获得这个RLock的线程释放。
"""
import threading
import time
import random


class Box(object):
    def __init__(self):
        self.lock = threading.RLock()
        self.total_items = 0

    def execute(self, value):
        with self.lock:
            self.total_items += value

    def add(self):
        with self.lock:
            self.execute(1)

    def remove(self):
        with self.lock:
            self.execute(-1)


def adder(box, items):
    print("N {} items to ADD\n".format(items))
    while items:
        box.add()
        time.sleep(1)
        items -= 1
        print("{}. ADDED one item --> {} item to ADD\n".format(box.total_items, items))


def remover(box, items):
    print("N {} items to REMOVE\n".format(items))
    while items:
        box.remove()
        time.sleep(1)
        items -= 1
        print("{} .REMOVED one item --> {} item to REMOVE\n".format(box.total_items, items))


def main():
    items = 10
    box = Box()
    t1 = threading.Thread(target=adder, args=(box, random.randint(10, 20)))
    t2 = threading.Thread(target=remover, args=(box, random.randint(0, 10)))

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == "__main__":
    main()

