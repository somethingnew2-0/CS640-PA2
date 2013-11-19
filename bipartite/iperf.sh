#!/bin/bash 
echo started iperf
iperf -c $1 -p 5001 -t 1 -i 1 -w 16m -Z reno > iperf.txt
echo iperf finished