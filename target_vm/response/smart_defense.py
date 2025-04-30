import pandas as pd
import subprocess
import time
import os
import psutil

LOG = "../monitoring/resource_log.csv"
ATTACKER_IP = "your-attacker-ip"        # Replace with your actual attacker's vm-ip
CPU_THRESHOLD = 70
NET_THRESHOLD = 100_000_000  # bytes per 8 sec
CHECK_INTERVAL = 2
RULES_APPLIED = False

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

def kill_high_cpu_processes(threshold=5):
    for proc in psutil.process_iter(['pid', 'cpu_percent']):
        if proc.info['cpu_percent'] > threshold:
            try:
                os.kill(proc.info['pid'], 9)
                print(f"[+] Killed process with high CPU: PID {proc.info['pid']}")
            except Exception as e:
                pass

def detect_and_respond():
    if not os.path.exists(LOG):
        return

    df = pd.read_csv(LOG)
    if len(df) < 5:
        return

    latest = df.tail(5)
    cpu_avg = latest['cpu'].mean()
    net_diff = latest['net_recv'].iloc[-1] - latest['net_recv'].iloc[0]

    if cpu_avg > CPU_THRESHOLD:
        print("[!] High CPU usage detected on VM")
        kill_high_cpu_processes()

    if net_diff > NET_THRESHOLD:
        print("[!] Network spike detected")
        apply_firewall_rules()

while True:
    detect_and_respond()
    time.sleep(CHECK_INTERVAL)

