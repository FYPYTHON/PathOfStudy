#!/bin/bash
a=7.0
b=100
aa=20
d=$(echo "$a*$b"|bc)
c=$(echo "$a*$b*$aa"|bc)
e=$(echo "$b/$a"|bc)
echo $d
echo $c
echo $e
t=$(echo "$a*$aa/100"|bc)
echo $t " t"
#echo int($a)

