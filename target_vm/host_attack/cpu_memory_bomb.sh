#!/bin/bash
# Heavy CPU and RAM Bomb on VM

echo "[*] Spawning heavy load processes..."

for i in {1..50}; do
    (yes > /dev/null &)  # Infinite yes loops
done

sleep 600
