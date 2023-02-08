#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/20 20:50
# @Author  : 1823218990@qq.com
# @File    : readme.py
# @Software: Pycharm


""""
# Group:
A group calls a list of tasks in parallel, and it returns a special result instance that lets you inspect the results as a group, and retrieve the return values in order.

from celery import group
from proj.tasks import add

group(add.s(i, i) for i in xrange(10))().get()
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

Partial group.
g = group(add.s(i) for i in xrange(10))
g(10).get()
[10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

"""

"""
# Chains:
Tasks can be linked together so that after one task returns the other is called:

from celery import chain
from proj.tasks import add, mul

# (4 + 4) * 8
chain(add.s(4, 4) | mul.s(8))().get()
64
or a partial chain:

# (? + 4) * 8
g = chain(add.s(4) | mul.s(8))
g(4).get()
64

Chains can also be written like this:

(add.s(4, 4) | mul.s(8))().get()
64
"""

"""
# Chords:

A chord is a group with a callback:

from celery import chord
from proj.tasks import add, xsum

chord((add.s(i, i) for i in xrange(10)), xsum.s())().get()
90
A group chained to another task will be automatically converted to a chord:

(group(add.s(i, i) for i in xrange(10)) | xsum.s())().get()
90
Since these primitives are all of the subtask type they can be combined almost however you want, e.g:

upload_document.s(file) | group(apply_filter.s() for filter in filters)
Be sure to read more about workflows in the Canvas user guide.
"""


"""
# Routing:
Celery supports all of the routing facilities provided by AMQP, but it also supports simple routing where messages are sent to named queues.

The CELERY_ROUTES setting enables you to route tasks by name and keep everything centralized in one location:

app.conf.update(
    CELERY_ROUTES = {
        'proj.tasks.add': {'queue': 'hipri'},
    },
)
You can also specify the queue at runtime with the queue argument to apply_async:

from proj.tasks import add
add.apply_async((2, 2), queue='hipri')
You can then make a worker consume from this queue by specifying the -Q option:

$ celery -A proj worker -Q hipri
You may specify multiple queues by using a comma separated list, for example you can make the worker consume from both the default queue, and the hipri queue, where the default queue is named celery for historical reasons:

$ celery -A proj worker -Q hipri,celery
The order of the queues doesn’t matter as the worker will give equal weight to the queues.

To learn more about routing, including taking use of the full power of AMQP routing, see the Routing Guide.
"""

"""
# Remote Control:
If you’re using RabbitMQ (AMQP), Redis or MongoDB as the broker then you can control and inspect the worker at runtime.

For example you can see what tasks the worker is currently working on:

$ celery -A proj inspect active
This is implemented by using broadcast messaging, so all remote control commands are received by every worker in the cluster.

You can also specify one or more workers to act on the request using the --destination option, which is a comma separated list of worker host names:

$ celery -A proj inspect active --destination=celery@example.com
If a destination is not provided then every worker will act and reply to the request.

The celery inspect command contains commands that does not change anything in the worker, it only replies information and statistics about what is going on inside the worker. For a list of inspect commands you can execute:

$ celery -A proj inspect --help
Then there is the celery control command, which contains commands that actually changes things in the worker at runtime:

$ celery -A proj control --help
For example you can force workers to enable event messages (used for monitoring tasks and workers):

$ celery -A proj control enable_events
When events are enabled you can then start the event dumper to see what the workers are doing:

$ celery -A proj events --dump
or you can start the curses interface:

$ celery -A proj events
when you’re finished monitoring you can disable events again:

$ celery -A proj control disable_events
The celery status command also uses remote control commands and shows a list of online workers in the cluster:

$ celery -A proj status
You can read more about the celery command and monitoring in the Monitoring Guide.
"""


def init():
    """
    一、Celery 对象解析
    我们先来看一下 Celery 的初始化方法：

    class Celery(object):
        def __init__(self, main=None, loader=None, backend=None,
                     amqp=None, events=None, log=None, control=None,
                     set_as_current=True, accept_magic_kwargs=False,
                     tasks=None, broker=None, include=None, changes=None,
                     config_source=None, fixups=None, task_cls=None,
                     autofinalize=True, **kwargs):

    常用的需要配置的参数：
    这些参数都是 celery 实例化的配置，我们也可以不写，可以使用config_from_object方法加载配置；

    main    : 如果作为__main__运行，则为主模块的名称。用作自动生成的任务名称的前缀
    loader  : 当前加载器实例。
    backend : 任务结果url；
    amqp    : AMQP对象或类名，一般不管；
    log     : 日志对象或类名；
    set_as_current : 将本实例设为全局当前应用
    tasks   : 任务注册表。
    broker  : 使用的默认代理的URL,任务队列；
    include : 每个worker应该导入的模块列表，以实例创建的模块的目录作为起始路径；
    """
    pass

def task_args():
    """
task的常用属性

    Task.name     : 任务名称；
    Task.request  : 当前任务的信息；
    Task.max_retries   : 设置重试的最大次数
    Task.throws        : 预期错误类的可选元组，不应被视为实际错误，而是结果失败；
    Task.rate_limit    : 设置此任务类型的速率限制
    Task.time_limit    : 此任务的硬限时（以秒为单位）。
    Task.ignore_result : 不存储任务状态。默认False；
    Task.store_errors_even_if_ignored : 如果True，即使任务配置为忽略结果，也会存储错误。
    Task.serializer    : 标识要使用的默认序列化方法的字符串。
    Task.compression   : 标识要使用的默认压缩方案的字符串。默认为task_compression设置。
    Task.backend       : 指定该任务的结果存储后端用于此任务。
    Task.acks_late     : 如果设置True为此任务的消息将在任务执行后确认 ，而不是在执行任务之前（默认行为），即默认任务执行之前就会发送确认；
    Task.track_started : 如果True任务在工作人员执行任务时将其状态报告为“已启动”。默认是False；

    """
    pass

def sync_task1():
    """
@celery.task
def function_name():
    pass

    """
    pass

def sync_task2():
    """
    @celery.task(bind=True, name='name')
    def function_name():
        pass

    # task方法参数
    name       : 可以显式指定任务的名字；默认是模块的命名空间中本函数的名字。
    serializer : 指定本任务的序列化的方法；
    bind       : 一个bool值，设置是否绑定一个task的实例，如果绑定，task实例会作为参数传递到任务方法中，可以访问task实例的所有的属性，即前面反序列化中那些属性
    base       : 定义任务的基类，可以以此来定义回调函数，默认是Task类，我们也可以定义自己的Task类
    default_retry_delay : 设置该任务重试的延迟时间，当任务执行失败后，会自动重试，单位是秒，默认3分钟；
    autoretry_for       : 设置在特定异常时重试任务，默认False即不重试；
    retry_backoff       : 默认False，设置重试时的延迟时间间隔策略；
    retry_backoff_max   : 设置最大延迟重试时间，默认10分钟，如果失败则不再重试；
    retry_jitter        : 默认True，即引入抖动，避免重试任务集中执行；


    # 当bind=True时，add函数第一个参数是self，指的是task实例
    @task(bind=True)  # 第一个参数是self，使用self.request访问相关的属性
    def add(self, x, y):
        try:
            logger.info(self.request.id)
        except:
            self.retry() # 当任务失败则进行重试，也可以通过max_retries属性来指定最大重试次数

    """
    pass


def sync_task3():
    """
    import celery

    class MyTask(celery.Task):
        # 任务失败时执行
        def on_failure(self, exc, task_id, args, kwargs, einfo):
            print('{0!r} failed: {1!r}'.format(task_id, exc))
        # 任务成功时执行
        def on_success(self, retval, task_id, args, kwargs):
            pass
        # 任务重试时执行
        def on_retry(self, exc, task_id, args, kwargs, einfo):
            pass

    @task(base=MyTask)
    def add(x, y):
        raise KeyError()

    # 方法相关的参数
    exc     : 失败时的错误的类型；
    task_id : 任务的id；
    args    : 任务函数的参数；
    kwargs  : 键值对参数；
    einfo   : 失败或重试时的异常详细信息；
    retval  : 任务成功执行的返回值


    """
    pass


def call_task1():
    """
方法一：app.send_task
    注意： send_task 在发送的时候是不会检查 tasks.add 函数是否存在的，即使为空也会发送成功，所以 celery 执行是可能找不到该函数报错；

    # File_name：tasks.py
    from celery import Celery

    app = Celery()

    def add(x, y):
        return x+y

    app.send_task('tasks.add',args=[3,4])  # 参数基本和apply_async函数一样

    :return:
    """
    pass


def call_task2():
    """
    Task.delay
    delay 方法是 apply_async 方法的简化版，不支持执行选项，只能传递任务的参数。

    from celery import Celery

    app = Celery()

    @app.task
    def add(x, y, z=0):

        return x + y

    add.delay(30, 40, z=5)	# 包括位置参数和关键字参数

    """
    pass


def call_task3():
    """
    Task.apply_async
    apply_async 支持执行选项，它会覆盖全局的默认参数和定义该任务时指定的执行选项，本质上还是调用了 send_task 方法；

    from celery import Celery

    app = Celery()

    @app.task
    def add(x, y, z=0):

        return x + y

    add.apply_async(args=[30,40], kwargs={'z':5})

    # 其他参数
    task_id   : 为任务分配唯一id，默认是uuid;
    countdown : 设置该任务等待一段时间再执行，单位为s；
    eta       : 定义任务的开始时间；eta=time.time()+10;
    expires   : 设置任务时间，任务在过期时间后还没有执行则被丢弃；
    retry     : 如果任务失败后, 是否重试;使用true或false，默认为true
    shadow    : 重新指定任务的名字str，覆盖其在日志中使用的任务名称；
    retry_policy : {},重试策略.如下：
        ----max_retries    : 最大重试次数, 默认为 3 次.
        ----interval_start : 重试等待的时间间隔秒数, 默认为 0 , 表示直接重试不等待.
        ----interval_step  : 每次重试让重试间隔增加的秒数, 可以是数字或浮点数, 默认为 0.2
        ----interval_max   : 重试间隔最大的秒数, 即 通过 interval_step 增大到多少秒之后, 就不在增加了, 可以是数字或者浮点数, 默认为 0.2 .

    routing_key : 自定义路由键；
    queue       : 指定发送到哪个队列；
    exchange    : 指定发送到哪个交换机；
    priority    : 任务队列的优先级，0到255之间，对于rabbitmq来说0是最高优先级；
    serializer  : 任务序列化方法；通常不设置；
    compression : 压缩方案，通常有zlib, bzip2
    headers     : 为任务添加额外的消息；
    link        : 任务成功执行后的回调方法；是一个signature对象；可以用作关联任务；
    link_error  : 任务失败后的回调方法，是一个signature对象；

    # 其他参数参考用法如下：
    add.apply_async((2, 2), retry=True, retry_policy={
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.2,
    })

"""
    pass