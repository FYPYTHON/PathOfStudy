#!/bin/bash
# 改密码
password="yourPass"
psql -h 127.0.0.1 -p 5866 -U syssso -d highgo -c "alter user test with password '$password';alter user test valid until 'infinity';"


# 连接
PGPASSWORD=${password} psql -h 127.0.0.1 -p 5866 -U test -d highgo


# list table
select tablename from pg_tables where schemaname='public';

# 密码锁住
psql -U syssso -h 127.0.0.1 -p 5866 -d highgo

# 查看密码锁
select clear_user_limit('test');

# 密码锁放开
select set_secure_param('hg_PwdErrorLock', '-1');
