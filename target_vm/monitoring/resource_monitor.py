import psutil
import time
import csv
from datetime import datetime

LOG_PATH = "resource_log.csv"

# Initialize the log file
with open(LOG_PATH, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "cpu", "mem", "net_sent", "net_recv"])

# Capture initial network stats
prev_net = psutil.net_io_counters()

while True:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    net = psutil.net_io_counters()
    net_sent = net.bytes_sent
    net_recv = net.bytes_recv

    with open(LOG_PATH, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, cpu, mem, net_sent, net_recv])

    time.sleep(1)

