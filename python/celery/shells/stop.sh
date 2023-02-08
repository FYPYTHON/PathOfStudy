#!/bin/bash

curdir=$(dirname $0)
cd $curdir
realdir=$(pwd)
echo $realdir
cd $realdir/../
chdir_path=$(pwd)
cd $chdir_path

cargs="-A src.mycelery.app -l info"
PYTHONPATH=${chdir_path}/lib/python3.8/site-packages ${chdir_path}/bin/celery multi stop worker ${cargs}

ps auxww | grep -v 'grep' | grep 'celery' | grep ' worker' | awk '{print $2}' | xargs kill -9


