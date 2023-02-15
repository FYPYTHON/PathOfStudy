# coding=utf-8
"""
https://pythonhosted.org/watchdog/quickstart.html
"""

import sys
sys.path.insert(0, "D:\project\lib\Lib\site-packages")
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
#
import threading
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff


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
        """
        windows 平台上每一次的文件修改引发两次 modified 事件 ?
        :param event:
        :return:
        """
        print(event)
        self.logger.info(self.fileNameList)
        if event.is_directory:
            self.logger.info("directory modified:{0}".format(event.src_path))
        else:
            self.logger.info("file modified:{0}".format(event.src_path))


class DiffWatchDog(FileSystemEventHandler):
    """
    snapshot 监控文件变化
    """
    def __init__(self, path):
        print("init DiffWatchDog: {}".format(path))
        FileSystemEventHandler.__init__(self)
        self.snapshot = DirectorySnapshot(path)
        self.timer = None
        self.path = path

    def heartbeat(self):
        if self.timer:
            # print("timer cancel")
            self.timer.cancel()
        self.check_snapshot()
        self.timer = threading.Timer(0.2, self.heartbeat)
        self.timer.start()
        # print("on_any_event")

    def check_snapshot(self):
        snapshot = DirectorySnapshot(self.path)
        diff = DirectorySnapshotDiff(self.snapshot, snapshot)
        self.snapshot = snapshot
        self.timer = None

        if diff.files_modified:
            print('files modified: {}'.format(diff.files_modified))
        # print('files created: {}'.format(diff.files_created))
        # print('files deleted: {}'.format(diff.files_deleted))
        # print('files modified: {}'.format(diff.files_modified))
        # print('files moved: {}'.format(diff.files_moved))

        # print('dirs created: {}'.format(diff.dirs_created))
        # print('dirs deleted: {}'.format(diff.dirs_deleted))
        # print('dirs modified: {}'.format(diff.dirs_modified))
        # print('dirs moved: {}'.format(diff.dirs_moved))


class TimedDirWatchDog(object):
    def __init__(self, path):
        print("init TimedDirWatchDog")
        self.path = path
        self.observer = Observer()

    def start(self):
        diff_watchdog_handler = DiffWatchDog(self.path)
        # self.observer.schedule(diff_watchdog_handler, self.path, recursive=True)
        # self.observer.start()
        # diff_watchdog_handler.check_snapshot()
        diff_watchdog_handler.heartbeat()

    def stop(self):
        self.observer.stop()


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


def monitor(path="."):
    mt = DiffWatchDog(path)
    mt.heartbeat()


if __name__ == "__main__":
    # path = sys.argv[1] if len(sys.argv) > 1 else '.'
    path = "D:\project\lib\example\watch_file"
    # run(path)
    monitor(path)