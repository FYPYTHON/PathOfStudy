# coding=utf-8
"""
windows使用Process会重新加载整个module
在windows上，子进程会自动import启动它的这个文件，而在import的时候是会自动执行这些语句的。如果不加__main__限制的化，就会无限递归创建子进程，进而报错。


main process start **
main process end
main process start **
  subprocess start
  subprocess end

"""

import multiprocessing
import time

print("main process start **")

def func():
    print("  subprocess start")
    time.sleep(3)
    print("  subprocess end")

p = multiprocessing.Process(target=func, name='my_sub')
p.start()

if __name__ == "__main__":
    # p = multiprocessing.Process(target=func, name='my_sub')
    # p.start()
    print('main process end')
