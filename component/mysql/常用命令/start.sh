#!/bin/bash

mkdir -p /opt/data/mysql
mkdir -p /opt/data/mariadb
if [ -L /tmp/mysql.sock ];then
    echo "exist"
else
    ln -s /opt/data/mysql/mysql.sock /tmp/mysql.sock
    echo "not exist"
fi

echo "must stop mysql first. "

echo "start mysql..."

/opt/mysql/bin/mysqld --defaults-file=/opt/midware/mysql/my.cnf --user=root &
