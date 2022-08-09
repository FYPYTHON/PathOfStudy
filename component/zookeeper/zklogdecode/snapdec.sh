#!/bin/bash

ori_file=$1
dec_file=$2

java -classpath /home/wgq/zklog/zookeeper-3.4.13.jar:/home/wgq/zklog/slf4j-api-1.7.25.jar:/home/wgq/zklog/slf4j-log4j12-1.7.25.jar:/home/wgq/zklog/log4j-1.2.17.jar org.apache.zookeeper.server.SnapshotFormatter  $1 > $2

