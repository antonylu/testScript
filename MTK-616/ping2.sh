#!/bin/bash

function elapsed_time()
{
    s_time=$1
    e_time=$2

    elap_s=$((e_time-s_time))
    ss=$((elap_s%60))
    mm=$(((elap_s/60)%60))
    hh=$((elaps/3600))
    printf "%i:%02i:%02i" $hh $mm $ss
}

begin_time=`date "+%s"`
s=0
i=0

now=$(date)

echo "$now"

while [ "$i" != "100" ]
do
    adb wait-for-devices
    adb shell ping 8.8.8.8
    sleep 1
done

now_time=`date "+%s"`
elap_time=`elapsed_time $begin_time $now_time`
echo "elapsed time=$elap_time"
