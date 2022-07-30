#!/bin/bash

cd /opt/mysql
bin/mysql -uroot -p$1 --connect-expired-password -e "set password=password('fy123456');"



