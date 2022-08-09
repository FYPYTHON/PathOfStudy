# coding=utf-8
# python3 -m pip install  psycopg2-binary
import psycopg2

host = '127.0.0.1'
user = 'test'
pwd = 'test'
port = 3314
table = 'emp'
database = 'repl'
SQL_TIMEOUT = 30
dbtype = 1

sql_conn = psycopg2.connect(host=host, port=port, user=user, password=pwd, database=database, connect_timeout=SQL_TIMEOUT)
cursor = sql_conn.cursor()


def get_data():
    cursor.execute("SELECT * from information_schema.tables where table_name='emp';")
    count = cursor.rowcount
    print("get data len is : {}".format(count))
    if count == 0:
        cursor.execute("CREATE TABLE emp (emp_first_name text, emp_last_name text, emp_salary numeric)")
        sql_conn.commit()
    one_data = cursor.fetchone()

    print(one_data)


def database_info():
    cursor.execute("select oid,datname from pg_database where datname='{table}';".format(table=table))
    one_data = cursor.fetchone()
    print("database at disk: ", one_data)
    cursor.execute("select pg_size_pretty(pg_database_size('{table}'));".format(table=table))
    one_data = cursor.fetchone()
    print("database size:", one_data)


def write_data(MAX=10**8):
    import random
    def get_randam_str(num):
        return ''.join(random.sample(
            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h',
             'g', 'f', 'e', 'd', 'c', 'b', 'a', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], num))

    for i in range(MAX):
        first_name = get_randam_str(20)
        last_name = get_randam_str(30)
        salary = str(random.randint(100000, 10000000))
        cursor.execute("insert into {} values ('{}', '{}', '{}')".format(table, first_name, last_name, salary))
        if i % 10000 == 0:
            print(MAX, i)
            sql_conn.commit()
    sql_conn.commit()


if __name__ == '__main__':
    database_info()
    get_data()
    write_data()