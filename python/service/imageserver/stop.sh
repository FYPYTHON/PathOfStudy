#!/bin/bash

# ps -ef | grep "imageserver" | grep -v grep | awk '{print $2}' | xargs kill -9


gi_pid=`pidof imageserver`
[ -z "${gi_pid}" ] && echo "imageserver is not running" || kill -9 ${gi_pid}

