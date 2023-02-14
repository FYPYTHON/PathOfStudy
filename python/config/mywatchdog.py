# coding=utf-8
# 2023-02-14
"""
https://pythonhosted.org/watchdog/quickstart.html
"""

import sys
sys.path.insert(0, "D:\project\lib\Lib\site-packages")
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler


def getLog(logfile="./mywatchdog.log", level=logging.DEBUG):
    logger = logging.getLogger()
    logger.setLevel(level)
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(logfile)
    fmt = logging.Formatter('[%(levelname)s]%(asctime)s %(filename)10s[%(lineno)s]- %(message)s')
    console_handler.setFormatter(fmt)
    file_handler.setFormatter(fmt)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.info("client start ...")
    return logger


class MyWatchDog(FileSystemEventHandler):
    """
    类属性中定义
    """
    fileNameList = []
    logger = getLog()

    def __int__(self):
        """
        watchdog 类内部不能使用自定义属性?
        :return:
        """
        self.logger.info("go 1")   # 不执行？
        FileSystemEventHandler.__init__(self)
        self.logger.info("go 2")   # 不执行？

    def on_moved(self, event):
        if event.is_directory:
            self.logger.info("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        else:
            self.logger.info("file moved from {0} to {1}".format(event.src_path, event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            self.logger.info("directory created:{0}".format(event.src_path))
        else:
            self.logger.info("file created:{0}".format(event.src_path))
            fileAllName = str(event.src_path.split('/')[-1])

            self.fileNameList.append(fileAllName)
            self.logger.info(self.fileNameList)

    def on_deleted(self, event):
        if event.is_directory:
            self.logger.info("directory deleted:{0}".format(event.src_path))
        else:
            self.logger.info("file deleted:{0}".format(event.src_path))
            if event.src_path in self.fileNameList:
                self.fileNameList.remove(event.src_path)

    def on_modified(self, event):
        print(event)
        self.logger.info(self.fileNameList)
        if event.is_directory:
            self.logger.info("directory modified:{0}".format(event.src_path))
        else:
            self.logger.info("file modified:{0}".format(event.src_path))


def run(path="."):
    watchdog_event_handler = MyWatchDog()
    # self.logger.info(dir(watchdog_event_handler))
    observer = Observer()
    observer.schedule(watchdog_event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    # path = sys.argv[1] if len(sys.argv) > 1 else '.'
    path = "D:\project\lib\example\watch_file"
    run(path)
