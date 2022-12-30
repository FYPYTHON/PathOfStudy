#!/bin/bash

user=super
pwd=Super#_@1230
# -u ${user} -p ${pwd}

# 单独启动某个程序

item=$1
if [ "$item"x == ""x ];then
   echo "stop none..."
   exit -1
fi
python_path=/opt/midware/python3.8
${python_path}/bin/supervisorctl -u ${user} -p ${pwd} -c ${python_path}/supervisord/supervisord.conf start $item

