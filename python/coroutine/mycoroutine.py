import asyncio

async def work(x):
    for _ in range(3):
        print("work {} is running...".format(x))
    return "Work {} is finished".format(x)


def call_back(future):
    print("callback:{}".format(future.result()))


corounine = work(1)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(corounine)
task.add_done_callback(call_back)
loop.run_until_complete(task)


