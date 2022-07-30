# coding=utf-8
from threading import Thread
from multiprocessing import Process
import time

"""
计算密集型任务，占用的是CPU的时间，Python多线程之间有一个调度问题，全局解释器锁GIL。
当有多个线程的时候，线程并不是并行在运行，他会申请一个全局解释器锁，谁申请到了，谁运行。
线程在串行运行，所以并没有加快。
Multi Threads
     Thread-1
1 Thread  run job need  5.038524150848389
     Thread-2
     Thread-3
2 Thread  run job need  5.062432289123535
     Thread-4
     Thread-5
     Thread-6
     Thread-7
4 Thread  run job need  5.061465263366699
     Thread-8
     Thread-9
     Thread-10
     Thread-11
     Thread-12
     Thread-13
6 Thread  run job need  5.042513608932495
20.204639809891084
Multi Process
     Process-1
1 Process  run job need  5.136265516281128
     Process-2
     Process-3
2 Process  run job need  2.6589195728302
     Process-4
     Process-5
     Process-6
     Process-7
4 Process  run job need  1.4344310760498047
     Process-8
     Process-9
     Process-10
     Process-11
     Process-12
     Process-13
6 Process  run job need  1.055178165435791
10.28580576300078

"""


def countdown(n):
    while n > 0:
        n -= 1


COUNT = 100000000


def thread_process_job(n, Thread_Process, job):
    """
    n: threads or processes
    Thread_Process: Thread／Process class
    job: job
    """
    local_time = time.time()

    threads_or_processes = [Thread_Process(target=job, args=(COUNT // n,)) for i in range(n)]
    for t in threads_or_processes:
        print("\t", t.name)
        t.start()
    for t in threads_or_processes:
        t.join()

    print(n, Thread_Process.__name__, " run job need ", time.time() - local_time)


if __name__ == "__main__":
    t1 = time.clock()
    print("Multi Threads")
    n_list = [1, 2, 4, 6]
    for i in n_list:
        thread_process_job(i, Thread, countdown)

    print(time.clock() - t1)

    t2 = time.clock()
    print("Multi Process")
    for i in n_list:
        thread_process_job(i, Process, countdown)
    print(time.clock() - t2)
