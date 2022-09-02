#!/bin/bash
cd /opt/midware/imageserver
./stop.sh
sleep 1
./start.sh
sleep 1
ps -ef | grep "imageserver"
