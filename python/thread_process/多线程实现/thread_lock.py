import threading
import time
import os
from threading import Thread
from random import randint

threadLock = threading.Lock()

class MyThreadClass(Thread):
    def __init__(self, name, duration):
        Thread.__init__(self)
        self.name = name
        self.duration = duration

    def run(self):
        threadLock.acquire()
        print("--->" + self.name + " running process ID" + str(os.getpid()))

        threadLock.release()

        time.sleep(self.duration)
        print("--->" + self.name + " over")

        # threadLock.release()

if __name__ == '__main__':
    start_time = time.time()
    thread1 = MyThreadClass("Thread#1", randint(1, 10))
    thread2 = MyThreadClass("Thread#2", randint(1, 10))
    thread3 = MyThreadClass("Thread#3", randint(1, 10))
    thread4 = MyThreadClass("Thread#4", randint(1, 10))
    thread5 = MyThreadClass("Thread#5", randint(1, 10))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()

    print("END")

    print("---- used %s seconds" % (time.time() - start_time))

