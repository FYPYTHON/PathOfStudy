#!/bin/bash
item=$1
python_path=/opt/midware/python3.8

user=super
pwd=Super#_@1230
# -u ${user} -p ${pwd}

if [ "$item"x == ""x ];then
    ${python_path}/bin/supervisorctl -u ${user} -p ${pwd} -c ${python_path}/supervisord/supervisord.conf stop all
    ${python_path}/bin/supervisorctl -u ${user} -p ${pwd} -c ${python_path}/supervisord/supervisord.conf shutdown
else
    ${python_path}/bin/supervisorctl -u ${user} -p ${pwd} -c ${python_path}/supervisord/supervisord.conf stop $item
fi
ps -ef | grep supervisord

