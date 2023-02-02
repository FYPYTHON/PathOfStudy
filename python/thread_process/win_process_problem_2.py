"""
multiprocessing.Pool报pickling error
现象
multiprocessing.Pool传递一个普通方法(不在class中定义的)时, 能正常工作.

from multiprocessing import Pool
 
p = Pool(3)
def f(x):
     return x*x
 
p.map(f, [1,2,3])
但在class中定义的方法使用multiprocessing.Pool会报pickling error错误.

报错代码
# coding: utf8
import multiprocessing
 
class MyTask(object):
    def task(self, x):
        return x*x
 
    def run(self):
        pool = multiprocessing.Pool(processes=3)
 
        a = [1, 2, 3]
        pool.map(self.task, a)
 
if __name__ == '__main__':
    t = MyTask()
    t.run()
会出现如下异常:

cPickle.PicklingError: Can't pickle <type 'instancemethod'>: attribute lookup __builtin__.instancemethod failed
原因:
stackoverflow上的解释:
Pool methods all use a queue.Queue to pass tasks to the worker processes. Everything that goes through the queue.Queue must be pickable. So, multiprocessing can only transfer Python objects to worker processes which can be pickled. Functions are only picklable if they are defined at the top-level of a module, bound methods are not picklable.


pool方法都使用了queue.Queue将task传递给工作进程。multiprocessing必须将数据序列化以在进程间传递。方法只有在模块的顶层时才能被序列化，跟类绑定的方法不能被序列化，就会出现上面的异常。

解决方法:

用线程替换进程
可以使用copy_reg来规避上面的异常.
dill 或pathos.multiprocesssing ：use pathos.multiprocesssing, instead of multiprocessing. pathos.multiprocessing is a fork of multiprocessing that uses dill. dill can serialize almost anything in python, so you are able to send a lot more around in parallel.
正确代码1

 # coding: utf8
from multiprocessing.pool import ThreadPool as Pool
 
class MyTask(object):
    def task(self, x):
        return x*x
 
    def run(self):
        pool = Pool(3)
 
        a = [1, 2, 3]
        ret = pool.map(self.task, a)
        print ret
 
if __name__ == '__main__':
    t = MyTask()
    t.run()
正确代码2:
# coding: utf8
import multiprocessing
import types
import copy_reg
 
def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)
 
copy_reg.pickle(types.MethodType, _pickle_method)
 
class MyTask(object):
    def __init__(self):
        self.__result = []
 
    def task(self, x):
        return x * x
 
    def result_collector(self, result):
        self.__result.append(result)
 
    def run(self):
        pool = multiprocessing.Pool(processes=3)
 
        a = [1, 2, 3]
        ret = pool.map(self.task, a)
        print ret
 
if __name__ == '__main__':
    t = MyTask()
    t.run()
python 2.7 类中使用多进程（multiprocessing）执行类函数时的问题
python 2.7 类中使用多进程（multiprocessing）执行类函数时报错

PicklingError: Can't pickle <type 'instancemethod'>: attribute lookup __builtin__.instancemethod failed

首先这是python2.7的一个bug,所以最简单的办法就是升级到python3

相关大神的文章的链接如下：

https://stackoverflow.com/questions/1816958/cant-pickle-type-instancemethod-when-using-multiprocessing-pool-map

http://bbs.chinaunix.net/thread-4111379-1-1.html

如果不升级python的话，就来改代码吧，我得改法如下：

import time
from multiprocessing import Pool
Class testClass():
    def upMethod(self):
        print '我是UP'
        time.sleep(1)
    def downMethod(self):
        print '我是DOWN'
        time.sleep(1)
  def multiProcess(self):
     p = Pool(2)
     aObj=p.apply_async(self, args=('up',))#这里是重点
     aObj=p.apply_async(self, args=('down',))#这里是重点
     p.close()
     p.join()
    def __call__(self,sign):#这里是重点
        if sign=='up':
                   return self.upMethod()
        elif sign=='down':
                   return self.downMethod()
if __name__=='__main__':
    testObj=testClass()
    testObj.multiProcess()
关于__call__的说明 http://www.cnblogs.com/superxuezhazha/p/5793536.html
"""
