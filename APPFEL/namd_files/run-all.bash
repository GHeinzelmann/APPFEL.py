#!/bin/bash

i=0
while [ $i -le RANGE ] ;
do
x=`printf "%02.0f" $i`
cd a$x 
namd2 +p6 conf_rest-00 > conf_rest-00.log
sleep 10
namd2 +p6 conf_rest-01 > conf_rest-01.log
cd ../
let i=$i+1
done

i=0
while [ $i -le RANGE ] ;
do
x=`printf "%02.0f" $i`
cd l$x 
namd2 +p6 conf_rest-00 > conf_rest-00.log
sleep 10
namd2 +p6 conf_rest-01 > conf_rest-01.log
cd ../
let i=$i+1
done

i=0
while [ $i -le RANGE ] ;
do
x=`printf "%02.0f" $i`
cd t$x 
namd2 +p6 conf_rest-00 > conf_rest-00.log
sleep 10
namd2 +p6 conf_rest-01 > conf_rest-01.log
cd ../
let i=$i+1
done

i=0
while [ $i -le RUMB ] ;
do
x=`printf "%02.0f" $i`
cd u$x 
namd2 +p6 conf_run-00 > conf_run-00.log
sleep 10
namd2 +p6 conf_run-01 > conf_run-01.log
cd ../
let i=$i+1
done

i=0
while [ $i -le RANGE ] ;
do
x=`printf "%02.0f" $i`
cd c$x 
namd2 +p6 conf_heat > conf_heat.log
sleep 10
namd2 +p6 conf_rest-00 > conf_rest-00.log
sleep 10
namd2 +p6 conf_rest-01 > conf_rest-01.log
cd ../
let i=$i+1
done

i=0
while [ $i -le RANGE ] ;
do
x=`printf "%02.0f" $i`
cd r$x 
namd2 +p6 conf_heat > conf_heat.log
sleep 10
namd2 +p6 conf_rest-00 > conf_rest-00.log
sleep 10
namd2 +p6 conf_rest-01 > conf_rest-01.log
cd ../
let i=$i+1
done


