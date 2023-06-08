#!/bin/bash

mkdir -p /home/test
cd /home/test
rm -rf /home/test/*.log
logfile="./ioinfocmd.log"
(
while true
do
   curmin=$(date "+%M")
   if [ "$curmin" -ge "57" ] || [ "$curmin" -lt "20" ];then
        echo -e "\n" &&  date >> $logfile
        echo "reach 57-20min start my function" >> $logfile
        echo "iostat" >> $logfile
       	iostat -t -kx 1 1 >> ./iostat.log
        echo "top" >> $logfile
        date >> ./top.log
	    top -b -d 1 -n 1 | head -40  >> ./top.log
        echo "iotop" >> $logfile
        date >> ./iotop.log
	    iotop -b -d 1 -n 1 | head -40 >> ./iotop.log
        echo "netstat" >> $logfile
        date >> ./net2171.log
        netstat -ntp | grep 2171 | grep TIME_WAIT >> ./net2171.log
		sleep 1
   else
      sleep 3
   fi
done
) >> $logfile 2>&1
