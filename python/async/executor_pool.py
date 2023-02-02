# coding=utf-8
# 1823218990@qq.com
# 2023-02-02

import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
TEST_NUM = 10

URLS = ['http://www.foxnews.com/',
            'http://www.cnn.com/',
            'http://europe.wsj.com/',
            'http://www.bbc.co.uk/',
            'http://some-made-up-domain.com/']


def func_test(*args, **kwargs):
    import urllib.request
    # Retrieve a single page and report the URL and contents
    print(args, kwargs)
    url = 'https://docs.python.org/zh-cn/3/library/concurrent.futures.html'
    with urllib.request.urlopen(url, timeout=30) as conn:
        return conn.read()


class ExecutorTask(object):
    def __init__(self, name, func, *args, **kwargs):
        self.name = name
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return "ExecutorTask({}, {}, {}, {})".format(self.name, self.func, self.args, self.kwargs)


class ConcurrentExecuter(object):
    def __init__(self, pool_executor='thread', max_workers=5):
        self.pool_executor = pool_executor
        self.max_workers = max_workers
        self.executor = None
        self.init_executor()

    def init_executor(self):
        if self.pool_executor == 'thread':
            self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        else:
            self.executor = ProcessPoolExecutor(max_workers=self.max_workers)

    def gene_task(self, func_test):
        self.tasks = []
        for i in range(TEST_NUM):
            self.tasks.append(ExecutorTask(str(i), func_test, i))
        return self.tasks

    def wait_on_future(self):
        t_start = time.time()
        with self.executor as et:
            future_task = [et.submit(task.func, task.args, task.kwargs) for task in self.tasks]
            for future in concurrent.futures.as_completed(future_task):
                # res = future_task[future]
                data = ''
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (data, exc))
                else:
                    print('%r page is %d bytes' % (data, len(data)))
        print("used: {}".format(time.time() - t_start))


if __name__ == '__main__':
    my_executor = ConcurrentExecuter()
    # my_executor = ConcurrentExecuter('process')
    my_executor.gene_task(func_test)
    my_executor.wait_on_future()
