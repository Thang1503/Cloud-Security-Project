import docker
import time
import csv
from datetime import datetime
import os

# === CONFIG ===
CONTAINER_NAME = "your-container-name"  # Replace with your container name
CSV_FILE = "container_resource_log.csv"
INTERVAL = 2  # seconds

# === INIT ===
client = docker.from_env()

def get_container_stats(container):
    try:
        stats = container.stats(stream=False)
        cpu_stats = stats["cpu_stats"]
        precpu_stats = stats["precpu_stats"]

        cpu_delta = cpu_stats["cpu_usage"]["total_usage"] - precpu_stats["cpu_usage"]["total_usage"]
        system_delta = cpu_stats["system_cpu_usage"] - precpu_stats["system_cpu_usage"]
        cpu_percent = 0.0
        if system_delta > 0 and cpu_delta > 0:
            cpu_percent = (cpu_delta / system_delta) * len(cpu_stats["cpu_usage"].get("percpu_usage", [1])) * 100.0

        mem_usage = stats["memory_stats"].get("usage", 0)
        mem_limit = stats["memory_stats"].get("limit", 1)
        mem_percent = (mem_usage / mem_limit) * 100.0

        net = stats.get("networks", {})
        rx = sum(interface.get("rx_bytes", 0) for interface in net.values())
        tx = sum(interface.get("tx_bytes", 0) for interface in net.values())

        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cpu_percent": round(cpu_percent, 2),
            "mem_percent": round(mem_percent, 2),
            "net_rx": rx,
            "net_tx": tx
        }

    except Exception as e:
        print(f"[ERROR] Failed to get stats: {e}")
        return None

def main():
    try:
        container = client.containers.get(CONTAINER_NAME)
    except docker.errors.NotFound:
        print(f"[-] Container '{CONTAINER_NAME}' not found.")
        return

    print(f"[+] Monitoring container '{CONTAINER_NAME}' every {INTERVAL} seconds...")

    # Create file if missing
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["timestamp", "cpu_percent", "mem_percent", "net_rx", "net_tx"])
        if not file_exists:
            writer.writeheader()
            file.flush()

        while True:
            stats = get_container_stats(container)
            if stats:
                writer.writerow(stats)
                file.flush()  # Ensure real-time update
            time.sleep(INTERVAL)

if __name__ == "__main__":
    main()

