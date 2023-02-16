#!/bin/bash

# celery -A tasks worker --loglevel=info
# -D  : 后台启动
# -c  : 并发数

curdir=$(dirname $0)
cd $curdir
realdir=$(pwd)
echo $realdir
cd $realdir/../
# root_dir=$(pwd)

# PYTHONPATH=/opt/midware/celery_main/lib/python3.8/site-packages 
# /opt/midware/celery_main/bin/celery -A /opt/midware/celery_main/src/tasks worker -l info -c2 -f %n-%i.log

# 后台启动multi: celery multi start w1 -A  CeleryPro -l info
# worker并发: --concurrency=10 -n worker2@%h

chdir_path=$(pwd)
cd $chdir_path

rm -rf *.log

echo $chdir_path >> ${chdir_path}/log.log
find $chdir_path -name __pycache__ -type d | xargs rm -rf

cargs="-A src.mycelery.app -l info --pidfile=${chdir_path}/worker.pid --logfile=${chdir_path}/log%I.log"
PYTHONPATH=${chdir_path}/lib/python3.8/site-packages ${chdir_path}/bin/celery multi start worker ${cargs}

cd -

