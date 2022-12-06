# coding=utf-8
from datetime import datetime
import threading
import queue
import time


def task(threadName, *args):
    print("threadName: {} real task {} ".format(threadName, args))
    time.sleep(2)
    return "ok"


class QueueThread(object):
    task_q = None

    def __init__(self, qsize=500, block=False, qtimeout=None, threads=5, logger=None):
        # threading.Thread.__init__(self)
        if logger is None:
            self.logger = object()
            self.logger_info = print
            self.logger_debug = print
            self.logger_error = print
        else:
            self.logger_info = logger.info
            self.logger_debug = logger.debug
            self.logger_error = logger.error
        self.qsize = qsize
        self.qtimeout = qtimeout
        self.threads = threads
        self.produce_status = True
        self.stop_flag = "exit"
        self.stop_status = False
        if not isinstance(self.task_q, queue.Queue):
            self.logger_info("init task queue")
            self.task_q = queue.Queue(self.qsize)

    def initLog(self, logger):
        pass

    def callback(self, res, st):
        """
        :param res: task result
        :param st:  task status
        :return:
        """
        self.logger_info("task callback status:{}, result:{}".format(st, res))

    def put(self, func, args, callback=None):
        task_info = (func, args, callback)
        self.logger_info("task_info: {}".format(task_info))
        if func == "exit":
            self.task_q.put(self.stop_flag)
        else:
            self.task_q.put(task_info)
        self.logger_info("put: {} to queue".format(task_info))

    def thread_init(self):
        for i in range(self.threads):
            t = threading.Thread(target=self.run, name="queue_thread_{}".format(i))
            t.start()

    def test_produce(self):
        self.produce_status = True
        for i in range(1000):
            self.put(task, (i,), False)
        qt.put("exit", "", True)
        self.produce_status = False

    def heart_beat(self):
        # test start
        test_produce = "test_produce"
        if test_produce not in threading.enumerate().__str__() and self.produce_status:
            self.logger_info("reinit {}".format(test_produce))
            t_p = threading.Thread(target=self.test_produce, name=test_produce)
            t_p.start()
        self.logger_info("{} run".format(test_produce))
        # test end

        self.logger_info("heartbeat start ... {}".format(datetime.now()))
        for i in range(self.threads):
            number = "queue_thread_{}".format(i)
            if number not in threading.enumerate().__str__():
                self.logger_info("{} not in thread list, then start again".format(number))
                t = threading.Thread(target=self.run, name="queue_thread_{}".format(i))
                t.start()

        if not self.stop_status:
            hb = threading.Timer(10, self.heart_beat)
            hb.start()
        else:
            self.logger_info("stop and exit")
            # threading.Event.set(self)
            exit(0)

    def run(self) -> None:
        # try:
        #     task = self.task_q.get_nowait()  # 不阻塞
        # except Exception as e:
        #     task = None
        cur_thread = threading.current_thread().getName()
        self.logger_info("cur_thread: {} run...".format(cur_thread))
        # self.logger_info(self.task_q)
        try:
            task = self.task_q.get(timeout=self.qtimeout)
        except queue.Empty as e:
            self.logger_error(e)
            task = self.stop_flag
        while task != self.stop_flag:
            func, args, cb = task
            try:
                result = func(cur_thread, *args)
                status = True
            except Exception as e:
                self.logger_error(e)
                result = None
                status = False
            if cb:
                try:
                    self.callback(result, status)
                except Exception as e:
                    self.logger_error(e)
            # if self.stop_status:
            #     task = self.stop_flag
            # else:
            #     task = self.task_q.get()
            try:
                task = self.task_q.get(timeout=self.qtimeout)
            except queue.Empty as e:
                self.logger_error(e)
            if task == self.stop_flag:
                self.stop_status = True
            if self.stop_status:
                break


if __name__ == '__main__':
    qt = QueueThread(qtimeout=5)
    qt.thread_init()
    qt.heart_beat()
    for i in range(5):
        qt.put(task, (i,), True)
    # qt.put("exit", "", True)
    # qt.thread_init()

