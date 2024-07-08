#!/bin/bash

rm -rf ./log/*

pid_info=$(ps -ef | grep sqlproxy| grep -v grep | awk '{print $2}')

if [ "$pid_info"x != "0"x ] && [ "$pid_info"x != ""x ];then
   echo "to kill $pid_info"
   kill -9 ${pid_info}
fi

ps -ef | grep sqlproxy| grep -v grep

