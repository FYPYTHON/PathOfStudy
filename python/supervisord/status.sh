#!/bin/bash

item=$1

python_path=/opt/midware/python3.8
${python_path}/bin/supervisorctl -c ${python_path}/supervisord/supervisord.conf status $item

