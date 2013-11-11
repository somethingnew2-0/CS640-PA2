#!/bin/bash 
if [ $1 = "s" ]
then
    echo starting server
    iperf -s -i 1 -w 16m &
else
    iperf -c $2 -t 5 -i 1 -w 16m -Z reno 
fi
