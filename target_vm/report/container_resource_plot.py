import pandas as pd
import matplotlib.pyplot as plt

# Config
LOG_PATH = "../monitoring/container_resource_log.csv"

# Load data
try:
    df = pd.read_csv(LOG_PATH)
except FileNotFoundError:
    print("[-] Log file not found. Make sure container_resource_log.csv exists.")
    exit(1)

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

# Normalize network I/O to MB
df['net_rx_MB'] = df['net_rx'] / (1024 * 1024)
df['net_tx_MB'] = df['net_tx'] / (1024 * 1024)

# Create subplots
fig, axs = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

# CPU Usage
axs[0].plot(df.index, df['cpu_percent'], color='red', label='CPU Usage (%)')
axs[0].set_ylabel('CPU (%)')
axs[0].set_ylim(0, 100)
axs[0].legend()
axs[0].grid(True)

# Memory Usage
axs[1].plot(df.index, df['mem_percent'], color='blue', label='Memory Usage (%)')
axs[1].set_ylabel('Memory (%)')
axs[1].set_ylim(0, 100)
axs[1].legend()
axs[1].grid(True)

# Network I/O
axs[2].plot(df.index, df['net_rx_MB'], color='green', label='Network RX (MB)')
axs[2].plot(df.index, df['net_tx_MB'], color='purple', label='Network TX (MB)')
axs[2].set_ylabel('Network I/O (MB)')
axs[2].legend()
axs[2].grid(True)

# X-axis label
plt.xlabel('Time')

# Title
plt.suptitle('Container Resource Usage Over Time', fontsize=16)

# Save to file
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("container_usage_graph.png")
print("[+] Graph saved as 'container_usage_graph.png'")

