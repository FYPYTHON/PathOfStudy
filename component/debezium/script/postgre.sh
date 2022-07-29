#!/bin/bash
rm -rf ./pg.log
./bin/connect-standalone.sh /opt/midware/kafka_2.13-2.4.0/config/connect-standalone.properties /opt/midware/kafka_2.13-2.4.0/config/postgres.properties >> ./pg.log  &
