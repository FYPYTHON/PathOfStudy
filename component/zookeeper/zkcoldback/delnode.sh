#!/bin/bash


export JAVA_HOME=/opt/midware/java/jdk1.8.0_221

/opt/midware/zookeeper/bin/zkCli.sh -server 127.0.0.1:2181 deleteall /node
/opt/midware/zookeeper/bin/zkCli.sh -server 127.0.0.1:2181 ls /


