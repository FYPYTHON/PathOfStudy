#!/bin/bash

ps -ef | grep get_master_from_zk | grep -v grep | awk '{print $2}' | xargs kill -9

python3.5 get_master_from_zk.py node1 &
python3.5 get_master_from_zk.py node2 &

