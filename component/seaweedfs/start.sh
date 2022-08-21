#!/bin/bash

nohup /opt/apps/seaweedfs/weed master -mdir=/opt/data/seaweedfs -port=9333 -defaultReplication=001 -ip=192.168.3.227 >>/opt/log/seaweedfs/master.log  &

nohup /opt/apps/seaweedfs/weed volume -dir=/opt/data/hd/hd0 -mserver=192.168.3.227:9333 -port 8081 -ip=192.168.3.227 >>/opt/log/seaweedfs/vol1.log &

nohup /opt/apps/seaweedfs/weed volume -dir=/opt/data/hd/hd1 -mserver=192.168.3.227:9333 -port 8082 -ip=192.168.3.227 >>/opt/log/seaweedfs/vol2.log &

nohup /opt/apps/seaweedfs/weed filer -master=192.168.3.227:9333 -ip=192.168.3.227 -defaultReplicaPlacement=001 &
