#!/bin/bash
# 运行中修改配置后，可此命令，不会全部重启


python_path=/opt/midware/python3.8
${python_path}/bin/supervisorctl -c ${python_path}/supervisord/supervisord.conf update



