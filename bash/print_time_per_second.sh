#!/bin/bash
# this script is used to print time every second

while [ true ]; do
    /bin/sleep 1
    time=$(date "+%Y-%m-%d %H:%M:%S")
    echo "${time}"
done
