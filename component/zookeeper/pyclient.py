# coding=utf-8
# 1823218990@qq.com
from kazoo.client import KazooClient
from datetime import datetime
import time
zk = KazooClient(hosts='192.168.3.222:2181')
zk.start()

def test(event):
    print('触发事件', datetime.now())

def main():
    try:
        msg = "{}".format(time.time())
        # zk.create('/testplatform/test', b'abc', makepath=True)
        vv = zk.get('/testplatform/test',watch = test)
        print("第一次获取value", vv[0])

        zk.create('/testplatform/test', b'abc', makepath=True)

        zk.set('/testplatform/test', msg.encode('utf-8'))
        zk.get('/testplatform/test',watch = test)
        print("第二次获取value")
        zk.create('/testp', b'abc', makepath=True)
        time.sleep(0.1)
        if zk.exists("/testp"):
            zk.delete('/testp')
    except Exception as e:
        # if zk.exists("/testp"):
        #     zk.delete('/testp')
        print(e)


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(e)
            break
    zk.stop()



