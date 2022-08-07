#!/bin/bash
#wget http://download.redis.io/releases/redis-5.0.5.tar.gz
#tar xzf redis-5.0.5.tar.gz
cd redis-5.0.5
#make
#make install

\cp ../redis_6379 /etc/init.d/
mkdir -p /etc/redis
mkdir -p /var/redis/6379
\cp ../6379.conf /etc/redis/6379.conf
cd /etc/init.d/
chkconfig redis_6379 on
service redis_6379 start
