# coding=utf-8
# 1823218990@qq.com
"""
https://stackoverflow.com/questions/30081961/multiprocessing-works-in-ubuntu-doesnt-in-windows
"""
import sys
import logging
import time
import multiprocessing
import threading
from queue import Queue
MIN_QUEUE_SIZE = 5


def test_func(*args, **kwargs):
    print("test_func run args is:", len(args), kwargs.keys())
    time.sleep(1)


def getLogger(console):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler("./process_queue_task.log")
    fmt = logging.Formatter('[%(levelname)s]%(asctime)s %(filename)10s[%(lineno)s]- %(message)s')
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(fmt)
        logger.addHandler(console_handler)
    return logger


class MyTask(object):
    def __init__(self, name, func, *args, **kwargs):
        self.name = name
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return "MyTask({}, {}, {}, {})".format(self.name, self.func, self.args, self.kwargs)
        # return "MyTask({}, {}, {})".format(self.name, self.func, self.args)


class ThreadQueueTask(object):
    def __init__(self, size=5, workers=4, name_prefix="Thread_", console=True):
        self.workers = workers if workers > 0 else 1
        self.task_queue = Queue(size if size > MIN_QUEUE_SIZE else MIN_QUEUE_SIZE)
        self.name_prefix = name_prefix
        self.console = console
        self.pool = []
        self.initLog()

    def initLog(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler("./thread_queue_task.log")
        fmt = logging.Formatter('[%(levelname)s]%(asctime)s %(filename)10s[%(lineno)s]- %(message)s')
        file_handler.setFormatter(fmt)
        self.logger.addHandler(file_handler)
        if self.console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(fmt)
            self.logger.addHandler(console_handler)
        # self.logger = getLogger(self.console)
        self.logger.info("ProcessQueueTask init ...")

    def init_workers(self):
        for i in range(self.workers):
            # windows下, target不能是本类自己的函数 ,如 self.execute_task
            # windows下, 使用logger会json序列化报错
            # 可以用 @staticmethod
            # if sys.platform.startswith("win"):
                # my_logger = getLogger(self.console)
            #     p_worker = threading.Thread(target=self.execute_task_static, args=(self.task_queue,))
            # else:
            #     p_worker = threading.Thread(target=self.execute_task)
            p_worker = threading.Thread(target=self.execute_task)
            p_worker.daemon = True
            p_worker.name = self.name_prefix + "_{}".format(i)
            self.pool.append(p_worker)
            p_worker.start()

    def gen_task(self):
        for i in range(30):
            task = MyTask("test", test_func, [i for i in range(i)], key=i, value=i+1)
            self.task_queue.put(task, block=True)

    def execute_task(self):
        while True:
            task = self.task_queue.get(block=True)
            if task is None:
                self.task_queue.put(task, block=True)
                break
            self.logger.info("{} task is: {}".format(threading.current_thread().name, task))
            if isinstance(task, MyTask):
                my_func = task.func
                args = task.args
                kwargs = task.kwargs
                my_func(args, kwargs)
            else:
                self.logger.error("unknown task type: {}".format(task))

    @staticmethod
    def execute_task_static(task_queue):
        print(threading.enumerate().__str__())
        logger = getLogger(True)
        while True:
            task = task_queue.get(block=True)
            if task is None:
                task_queue.put(task, block=True)
                break
            logger.info("{} task is: {}".format(threading.current_thread().name, task))
            if isinstance(task, MyTask):
                my_func = task.func
                args = task.args
                kwargs = task.kwargs
                my_func(args, kwargs)
            else:
                logger.error("unknown task type: {}".format(task))
                pass

    def wait_for_finish(self):
        for process in self.pool:
            if process.is_alive():
                process.join()

    def job_run(self):
        t_start = time.time()
        self.init_workers()
        self.logger.info("init_workers ok...")
        self.gen_task()
        self.logger.info("gen_task ok...")
        self.task_queue.put(None, block=True)
        self.logger.info("set end flag ok...")
        self.wait_for_finish()
        self.logger.info("wait_for_finish ok...")
        self.logger.info("used time: {}".format(time.time() - t_start))


class ProcessQueueTask(object):
    def __init__(self, size=5, workers=4, name_prefix="Process_", console=True):
        self.workers = workers if workers > 0 else 1
        self.task_queue = multiprocessing.Manager().Queue(size if size > MIN_QUEUE_SIZE else MIN_QUEUE_SIZE)
        self.name_prefix = name_prefix
        self.console = console
        self.pool = []
        self.initLog()

    def initLog(self):
        # self.logger = logging.getLogger()
        # self.logger.setLevel(logging.INFO)
        # file_handler = logging.FileHandler("./process_queue_task.log")
        # fmt = logging.Formatter('[%(levelname)s]%(asctime)s %(filename)10s[%(lineno)s]- %(message)s')
        # file_handler.setFormatter(fmt)
        # self.logger.addHandler(file_handler)
        # if self.console:
        #     console_handler = logging.StreamHandler()
        #     console_handler.setFormatter(fmt)
        #     self.logger.addHandler(console_handler)
        self.logger = getLogger(self.console)
        self.logger.info("ProcessQueueTask init ...")

    def init_workers(self):
        for i in range(self.workers):
            # windows下, target不能是本类自己的函数 ,如 self.execute_task
            # windows下, 使用logger会json序列化报错
            # 可以用 @staticmethod
            if sys.platform.startswith("win"):
                # my_logger = getLogger(self.console)
                p_worker = multiprocessing.Process(target=self.execute_task_static, args=(self.task_queue,))
            else:
                p_worker = multiprocessing.Process(target=self.execute_task)
            p_worker.daemon = True
            p_worker.name = self.name_prefix + "_{}".format(i)
            self.pool.append(p_worker)
            p_worker.start()

    def gen_task(self):
        for i in range(30):
            task = MyTask("test", test_func, [i for i in range(i)], key=i, value=i+1)
            self.task_queue.put(task, block=True)

    def execute_task(self):
        while True:
            task = self.task_queue.get(block=True)
            if task is None:
                self.task_queue.put(task, block=True)
                break
            self.logger.info("{} task is: {}".format(multiprocessing.current_process().name, task))
            if isinstance(task, MyTask):
                my_func = task.func
                args = task.args
                kwargs = task.kwargs
                my_func(args, kwargs)
            else:
                self.logger.error("unknown task type: {}".format(task))

    @staticmethod
    def execute_task_static(task_queue):
        logger = getLogger(True)
        while True:
            task = task_queue.get(block=True)
            if task is None:
                task_queue.put(task, block=True)
                break
            logger.info("{} task is: {}".format(multiprocessing.current_process().name, task))
            if isinstance(task, MyTask):
                my_func = task.func
                args = task.args
                kwargs = task.kwargs
                my_func(args, kwargs)
            else:
                logger.error("unknown task type: {}".format(task))
                pass

    def wait_for_finish(self):
        for process in self.pool:
            if process.is_alive():
                # print(process)
                process.join()

    def job_run(self):
        t_start = time.time()
        self.init_workers()
        self.logger.info("init_workers ok...")
        self.gen_task()
        self.logger.info("gen_task ok...")
        self.task_queue.put(None, block=True)
        self.logger.info("set end flag ok...")
        self.wait_for_finish()
        self.logger.info("wait_for_finish ok...")
        self.logger.info("used time: {}".format(time.time() - t_start))


if __name__ == '__main__':
    s = ThreadQueueTask()
    s.job_run()

    # t = ProcessQueueTask()
    # t.job_run()
