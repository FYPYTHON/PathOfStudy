#!/bin/bash
:<<!
AiData  meetingData  mtLog  platformData  platformLog
./ddtest.sh hd0 AiData 1 5
!
echo $1 $2 $3 $4
for i in $(seq $3 $4);
do
  echo $i $4;
  name="$i.test.bin"
  echo $name
  dd if=/dev/sda of=/opt/data/hd/$1/$2/$name bs=1G count=1
  echo /opt/data/hd/$1/$2/$name
  echo $?
done
