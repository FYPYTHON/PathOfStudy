import tormysql
from tormysql import DictCursor
from tornado.ioloop import IOLoop
from tornado import gen
import time
pool = tormysql.helpers.ConnectionPool(
    max_connections=20,  # max open connections
    idle_seconds=20,  # conntion idle timeout time, 0 is not timeout
    # 源码pool.py 113行 min(self._idle_seconds, 60),  -- 超时最大值为60s.
    wait_connection_timeout=2,  # wait connection timeout
    host="172.16.80.191",port=3306,user="kedacom",passwd="Keda!Mysql_36",charset="utf8"
)
@gen.coroutine
def test():
    args = (0,)
    with (yield pool.Connection()) as conn:
        try:
            with conn.cursor(cursor_cls=DictCursor) as cursor:
                print(conn.__connections)
                yield cursor.execute("show variables like '%timeout%';")
                datas = cursor.fetchall()
                import json
                print(json.dumps(datas, indent=4))
                yield cursor.execute("select sleep(305);")
                datas = cursor.fetchall()
        except Exception as e:
            print("Query error: %s" % e)
        else:
            yield conn.commit()



t_start = time.time()
ioloop = IOLoop.instance()
ioloop.run_sync(test)

print("used: ", time.time() - t_start)