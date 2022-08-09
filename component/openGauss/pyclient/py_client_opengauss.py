#!/opt/midware/python3/bin/python3
# coding=utf-8

import sys
sys.path.append("/home/py-opengauss/lib/python3.5/site-packages")

import random
def get_randam_str(num):
    return ''.join(random.sample(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h',
         'g', 'f', 'e', 'd', 'c', 'b', 'a', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], num))


def make_data(make_gs):
    first_name = get_randam_str(20)
    last_name = get_randam_str(30)
    salary = str(random.randint(100000, 10000000))
    make_gs(first_name, last_name, salary)

import py_opengauss
### pq://user:password@host:port,host:port/database
### db = py_opengauss.open('opengauss://user:password@host:port/database')
### db = py_opengauss.open('opengauss://user:password@host1:123,host2:456/database')
### db = py_opengauss.open('localhost/postgres')
### engine = create_engine('postgresql+pyopengauss://user:password@host1:port1,host2:port2/db')

user = 'test'
pwd = '2022@test'
host = '127.0.0.1'
port = 5432
dbname = 'repl'

db = py_opengauss.open('pq://{user}:{pwd}@{host}:{port}/{dbname}'.format(user=user, pwd=pwd, host=host, port=port, dbname=dbname))

db.execute("SELECT * from information_schema.tables;")
emp_info = db.execute("SELECT * from information_schema.tables where table_name='emp';")
print(emp_info)
db.execute("CREATE TABLE emp (emp_first_name text, emp_last_name text, emp_salary numeric)")

make_emp = db.prepare("INSERT INTO emp VALUES ($1, $2, $3)")
MAX = 10**8



# make_emp("John", "Doe", "75322")   # 必须先？
make_data(make_emp)
with db.xact():
    for i in range(MAX):
        # first_name = get_randam_str(20)
        # last_name = get_randam_str(30)
        # salary = str(random.randint(100000, 10000000))
        # make_emp(first_name, last_name, salary)
        make_data(make_emp)
        # make_emp("Edward", "Johnson", "82744")


# python3 -m py_opengauss.bin.pg_python -h localhost -p port -U theuser -d database_name
# /opt/midware/python3/bin/python3 -m py_opengauss.bin.pg_python -h 127.0.0.1 -p 5432 -U test -d postgres -W -m timeit -s "ps=prepare('select 1')" "ps.first()"


