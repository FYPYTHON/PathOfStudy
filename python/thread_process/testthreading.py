import threading
from threading import Thread
from multiprocessing import Process
import time
from datetime import datetime
import os


def timed_task():
    # sleep_time = 10
    # while True:
    #     print("bcstatus start...")
    #     sdata = get_status()
    #     write_basecloud_warning(sdata)
    #     time.sleep(sleep_time)
    print(datetime.now(), "bcstatus start...", os.getpid())
    time.sleep(30)
    print(datetime.now(), "bcstatus end...", os.getpid())


def main_thread():
    import threading
    from threading import Timer
    # os.system("rm -rf /opt/log/basecloud/status_basecloud.log")
    is_daemon = True
    # import multiprocessing
    # multiprocessing.Process(target=timed_task, name='bcstatus', daemon=is_daemon).start()
    t = threading.Thread(target=timed_task, name='bcstatus', daemon=is_daemon)
    t.start()
    # t.join()
    # timed_task()
    # task = Timer(10, main_thread)
    # task.start()


if __name__ == "__main__":
    print("start...")
    # main_thread()
    import threading
    while True:
        print(datetime.now(), "bcstatus thread: {}".format(threading.enumerate().__str__()))
        # print(threading.enumerate().__str__())
        if "bcstatus" not in threading.enumerate().__str__():
            # main_thread()
            t = threading.Thread(target=timed_task, name='bcstatus', daemon=True)
            t.start()
        else:
            print(datetime.now(), "bcstatus thread running, then wait")
        print(datetime.now(), "end...")
        time.sleep(10)
    # print("stop...")
