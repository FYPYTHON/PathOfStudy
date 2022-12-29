#!/bin/bash

item=$1
python_path=/opt/midware/python3.8
if [ "itme"x == ""x ];then

    ${python_path}/bin/supervisord -c ${python_path}/supervisord/supervisord.conf
else
    ${python_path}/bin/supervisorctl -c ${python_path}/supervisord/supervisord.conf start $item
fi


