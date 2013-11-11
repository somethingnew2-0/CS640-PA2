#!/bin/bash 
if [ $1 = "s" ]
then
    echo starting server
    iperf -s -t 1 -i 1 -w 16m 
    echo stopping server
else
    iperf -c $2 -t 1 -i 1 -w 16m -Z reno 
fi
