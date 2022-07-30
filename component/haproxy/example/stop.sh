#!/bin/bash

pids=$(ps -ef | grep haproxy | grep -v "grep" | awk '{print $2}'|xargs)
echo $pids
kill -9 $pids
echo "haproxy stop..."
echo $?
