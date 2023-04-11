#!/bin/bash

echo $1

ps -ef | grep "$1"
pids=$(ps -ef | grep "$1" | grep -v "killm.sh"| grep -v "grep" | awk '{print $2}'|xargs)

echo $pids
kill -9 $pids
echo $1 " stop..."
echo $?
