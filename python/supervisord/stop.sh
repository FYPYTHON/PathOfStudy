#!/bin/bash
item=$1
python_path=/opt/midware/python3.8

if [ "$item"x == ""x ];then
    ${python_path}/bin/supervisorctl -c ${python_path}/supervisord/supervisord.conf stop all
    ${python_path}/bin/supervisorctl -c ${python_path}/supervisord/supervisord.conf shutdown
else
    ${python_path}/bin/supervisorctl -c ${python_path}/supervisord/supervisord.conf stop $item
fi
ps -ef | grep supervisord

