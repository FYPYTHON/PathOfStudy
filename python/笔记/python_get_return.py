# coding=utf-8

import os
res = os.system("percent_space=$(df /root | awk 'END{print $5}' | tr -d '%');exit $percent_space")
code = res >> 8



code, msg = subcommand("redis-benchmak 2>&1")
# 命令带上 2>&1, 将命令打印信息输出到msg

