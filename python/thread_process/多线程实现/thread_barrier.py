# coding=utf-8
from random import randrange
from threading import Barrier, Thread
from time import ctime, sleep

"""
如果一个进程的所有线程没有全部完成他们的任务，进程就不能继续。
屏障（barrier）实现了这个概念：如果一个线程完成了他的阶段，会调用一个屏障原语并停止。
涉及的所有线程都完成其执行阶段而且都调用了屏障原语时，系统将他们全部解锁，允许这些线程进入下一个阶段。
"""

num_runners = 3
finish_line = Barrier(num_runners)

runners = ["Huey", "Dewey", "Louie"]


def runner():
    name = runners.pop()
    sleep(randrange(2, 5))
    print("{} reached the barrier at : {}\n".format(name, ctime()))
    finish_line.wait()


def main():
    threads = []
    print("START RACE!!!")
    for i in range(num_runners):
        threads.append(Thread(target=runner))
        threads[-1].start()
    for thread in threads:
        thread.join()
    print("Race over!")


if __name__ == '__main__':
    main()
