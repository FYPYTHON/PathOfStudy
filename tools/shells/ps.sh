#!/bin/bash

while true
do
#   ps -ef | grep -v grep | grep grub | grep set >> /home/testps.log
#done
date >> /home/testps.log
oupid=$(ps -ef | grep /usr/lib/systemd/systemd | grep -v grep | grep omm | awk '{print $2}')
strace -ttt -T -e trace=all -f -s 1024 -o /home/starce.log -p $oupid

hasRun=$(ps aux | grep -v grep | grep "/home/ps.sh" | wc -l)
if [ ${hasRun} -lt 3 ];then
    echo "ps.sh is running"
    ps -ef | grep ps.sh
fi
done
