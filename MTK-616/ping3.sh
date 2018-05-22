#!/bin/bash
echo "Start from $(date)" > /sdcard/ping.log
ping -c 10000 8.8.8.8 | while read ping; do echo "$(date +"%m-%d %X"): $ping"  ; done | tee -a /sdcard/ping.log &
