import pandas as pd
import time
from datetime import datetime
import subprocess
import docker
import os

# === CONFIG ===
LOG = "../monitoring/container_resource_log.csv"
ATTACKER_IP = "your-attacker-ip"        # Replace with your actual attacker's vm-ip
CONTAINER_NAME = "your-container-name"  # Replace with actual container name
CPU_THRESHOLD = 70.0                    # %
NET_RX_THRESHOLD = 150_000_000          # bytes over 10 seconds
CHECK_INTERVAL = 2                      # seconds
WINDOW = 5                              # number of recent samples (5 x 2s = 10s)
RULES_APPLIED = False


# === INIT ===
client = docker.from_env()
try:
    container = client.containers.get(CONTAINER_NAME)
except docker.errors.NotFound:
    print(f"[-] Container '{CONTAINER_NAME}' not found.")
    exit(1)

def detect_cpu_attack(df):
    cpu_avg = df["cpu_percent"].mean()
    if cpu_avg > CPU_THRESHOLD:
        print(f"[!] High CPU detected in container: avg {cpu_avg:.2f}% > {CPU_THRESHOLD}%")
        return True
    return False

def detect_network_attack(df):
    net_diff = df["net_rx"].iloc[-1] - df["net_rx"].iloc[0]
    if net_diff > NET_RX_THRESHOLD:
        print(f"[!] High Network RX detected in container: +{net_diff:.2f} MB in {WINDOW * CHECK_INTERVAL}s")
        return True
    return False

def apply_firewall_rules():
    global RULES_APPLIED
    if RULES_APPLIED:
        return
    print("[+] Applying advanced firewall hardening rules")
    subprocess.run(["sudo", "sysctl", "-w", "net.ipv4.tcp_syncookies=1"])
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ATTACKER_IP, "-j", "DROP"])
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--syn", "-m", "connlimit", "--connlimit-above", "30", "-j", "REJECT"])
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--dport", "80", "-m", "limit", "--limit", "20/s", "--limit-burst", "100", "-j", "ACCEPT"])
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-m", "state", "--state", "INVALID", "-j", "DROP"])
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "-m", "limit", "--limit", "25/s", "--limit-burst", "100", "-j", "ACCEPT"])
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "-j", "DROP"])
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-f", "-j", "DROP"])
    RULES_APPLIED = True

def restart_container():
    try:
        container.restart()
        print(f"[+] Restarted container '{CONTAINER_NAME}' to mitigate attack.")
    except Exception as e:
        print(f"[ERROR] Failed to restart container: {e}")

def main():
    print(f"Started container defense monitor for '{CONTAINER_NAME}'")

    while True:
        if not os.path.exists(LOG):
            print(f"[WARN] Log file '{LOG}' not found. Waiting...")
            time.sleep(CHECK_INTERVAL)
            continue

        try:
            df = pd.read_csv(LOG)
            if len(df) < WINDOW:
                time.sleep(CHECK_INTERVAL)
                continue

            latest = df.tail(WINDOW)

            # Detection
            cpu_alert = detect_cpu_attack(latest)
            net_alert = detect_network_attack(latest)

            if cpu_alert:
                restart_container()
                
            if net_alert:
                apply_firewall_rules()

        except Exception as e:
            print(f"[ERROR] Exception while processing: {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

