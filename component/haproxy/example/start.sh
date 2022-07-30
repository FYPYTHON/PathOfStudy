#!/bin/bash
mkdir -p /var/lib/haproxy
/opt/apps/ha/sbin/haproxy -f /opt/apps/ha/conf/haproxy.cfg >>/opt/apps/ha/shell/ha.log

# 多个配置
/opt/apps/ha/sbin/haproxy -f /opt/apps/ha/conf/ >>/opt/apps/ha/shell/ha.log

echo $?
