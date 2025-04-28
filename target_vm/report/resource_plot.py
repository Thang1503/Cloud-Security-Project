import pandas as pd
import matplotlib.pyplot as plt

# Path to the resource log
log_path = "../monitoring/resource_log.csv"

# Load data
try:
    df = pd.read_csv(log_path)
except FileNotFoundError:
    print("[-] resource_log.csv not found!")
    exit(1)

# Convert timestamp to datetime if it's not already
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Set timestamp as index for better plotting
df.set_index('timestamp', inplace=True)

# Create a figure with 3 subplots (CPU, Memory, Network)
fig, axs = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

# Plot CPU Usage
axs[0].plot(df.index, df['cpu'], color='red', label='CPU Usage (%)')
axs[0].set_ylabel('CPU Usage (%)')
axs[0].set_ylim(0, 100)
axs[0].legend()
axs[0].grid(True)

# Plot Memory Usage
axs[1].plot(df.index, df['mem'], color='blue', label='Memory Usage (%)')
axs[1].set_ylabel('Memory Usage (%)')
axs[1].set_ylim(0, 100)
axs[1].legend()
axs[1].grid(True)

# Plot Network Received (normalized to MB for easier view)
axs[2].plot(df.index, df['net_recv'] / (1024*1024), color='green', label='Network Received (MB)')
axs[2].set_ylabel('Network Received (MB)')
axs[2].legend()
axs[2].grid(True)

# Common X-axis label
plt.xlabel('Time')

# Title
plt.suptitle('System Resource Usage Over Time', fontsize=16)

# Layout adjustments
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Save the plot
plt.savefig('resource_usage_graph.png')
print("[+] Graph saved as 'resource_usage_graph.png'")
