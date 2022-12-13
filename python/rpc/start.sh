#!/bin/bash

curdir=$(dirname $0)
cd $curdir

./stop.sh

/opt/midware/python3/bin/python3 rpyc_server.py &


