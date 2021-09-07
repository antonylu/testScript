#!/bin/sh
#
# Stability test of switch Camera Photo/Video Preview mode
# 
# Sending touch taps on specific coordinates on 10" Argon2 tablet
# Switch back and forth every 2x2 seconds
#
# adb push *.sh /data/
# adb shell chmod 755 /data/*.sh
#
# after test
#  adb shell getprop persist.camera.count
# 
count=1
while true
do
    echo $count
    setprop persist.camera.count $count
    count=$(($count+1))
    input tap 1247 486
    sleep 2
    input tap 1247 486
    sleep 2
done
