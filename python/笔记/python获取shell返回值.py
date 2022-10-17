# coding=utf-8

import os
res = os.system("percent_space=$(df /root | awk 'END{print $5}' | tr -d '%');exit $percent_space")
code = res >> 8