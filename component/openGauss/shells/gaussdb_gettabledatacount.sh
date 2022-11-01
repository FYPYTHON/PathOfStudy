#!/bin/bash

dbname=$1
port=5432
user=omm
pwd="mypwd"
if [ "$dbname"x == ""x ];then
    dbname=postgres
fi
(

source /home/omm/.bashrc

tables=$(gsql -r -d postgres -p ${port} -U ${omm} -W ${pwd} -d $dbname -c "select tablename from pg_tables\x on" | grep tablename | awk '{print $3}' | xargs)

for table in ${tables[*]}
do
   echo $table | grep pg_  2>&1 >/dev/null
   res=$?
   if [ "$res"x == "0"x ];then
       continue
   fi
   t_count=$(gsql -r -d postgres -p ${port} -U ${omm} -W ${pwd} -d $dbname -c "select count(*) from $table\x on" | grep count | awk '{print $3}' 2>/dev/null)
   if [ "$t_count" -gt "0" ];then
        echo $table $t_count
   fi
   t_count=0
done 
) 2>/dev/null


