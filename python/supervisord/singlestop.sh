#!/bin/bash

# 单独停止某个程序

item=$1
if [ "$item"x == ""x ];then
   echo "stop none..."
   exit -1
fi
python_path=/opt/midware/python3.8
${python_path}/bin/supervisorctl -c ${python_path}/supervisord/supervisord.conf stop $item

