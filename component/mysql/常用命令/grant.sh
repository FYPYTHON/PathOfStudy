#!/bin/bash

password='1234'
# remote
mysql -uroot -p$password --connect-expired-password -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '$password';flush privileges;"

# repl
/opt/midware/mysql/bin/mysql -uroot -p$password --connect-expired-password -e "create user repl;GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%.%.%.%' IDENTIFIED BY '$1';flush privileges;"
