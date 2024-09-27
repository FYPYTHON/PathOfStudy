# coding=utf-8
# 1823218990@qq.com

import sys
import psycopg2


class ClientPsycopg2(object):
    def __init__(self, host="127.0.0.1", port=3306, password="test", user="test",
                 database="postgres", timeout=10, logger=None):
            self.sqlclient = psycopg2.connect(host=host, port=port, user=user, password=password,
                                              database=database,
                                              connect_timeout=timeout,
                                              options='-c statement_timeout={}s'.format(timeout))
            self.cursor = self.sqlclient.cursor()
            self.sqlclient.autocommit = True
            # self.cursor.execute("set statement_timeout='{}s'".format(timeout))

    def run(self):
        # self.cursor.execute("select sleep 60;")
        self.cursor.execute("select pg_sleep(60);")


if __name__ == '__main__':
    client = ClientPsycopg2()
    client.run()
