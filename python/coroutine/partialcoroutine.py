from functools import partial

def func(a, b):
    return a + b

# normal
result = func(1, 2)

# partial
new_func = partial(func, 1)   # first args is fixed, just input second args
result2 = new_func(2)

print(result, result2)

import asyncio

async def work(x):
    for _ in range(3):
        print("work {} is running...".format(x))
    return "Work {} is finished".format(x)


def call_back(num, future):
    print("callback:{}, the num is :{}".format(future.result(), num))


corounine = work(1)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(corounine)
task.add_done_callback(partial(call_back, 5))
loop.run_until_complete(task)


