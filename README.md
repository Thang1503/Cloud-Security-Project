# VM Tsunami: A Flooded Attack
Cloud Security Project - Spring 2025

## Overview
This project simulates various **network-based** and **host-based** attacks targeting a virtual machine and a Docker container, with real-time monitoring, detection, automated defense, and reporting mechanisms.

The project uses:
- **Resource monitoring** to track CPU, Memory, and Network I/O
- **Automated detection and defense** against high CPU or network spikes
- **Attack scripts** to simulate heavy flooding and resource exhaustion
- **Reporting tools** to visualize resource usage during attacks

---

## Project Structure

| Folder | Description |
|--------|-------------|
| `attack_vm/` | Contains network-based attack scripts launched from the Attacker VM |
| `target_vm/monitoring/` | Resource monitoring script for the Target VM |
| `target_vm/response/` | Smart detection and defense script for automated protection |
| `target_vm/host-attack/` | Contains host-based attack scripts launched from the Target VM |
| `target_vm/report/` | Script to generate graphs from monitoring logs |

---

## How to Run the Project

### 1. Set up the Environment
- Two VirtualBox VMs: **Attacker VM** and **Target VM**
- Each VM needs to have at least 2 CPU's core, 4 GB RAM, and 25 GB of Disk Memory. Both VM used Bridge Network
- The tools used in both VMs are: hping3, Scapy, psutil, pandas, matplotlib, htop, and docker
- The docker container inside the Target VM needs to be build and configure in a specific way for the attack to work properly.
- Docker set up:
    - Build an image using the Dockerfile provided in the target_vm folder: "docker build -t <your-image-name> ."
    - Run the container, mapping port 80 UDP: "docker run -dit --name <your-container-namee> -p 80:80/udp <your-image-name>"


### 2. Run Monitoring on Target VM
- There are two different monitoring scripts: **resource_monitor.py** and **container_monitor.py**
- Run the **resource_monitor.py** when launching an attack on the VM, and **container_monitor.py** when launching an attack on the container
- Before running the **container_monitor.py** script, please go into the script and edit the CONTAINER_NAME to your own container's name
cd Cloud-Security-Project/target_vm/monitoring
sudo python3 resource_monitor.py **or**
sudo python3 container_monitor.py

### 3. Run Defense on Target VM
- There are two different defense scripts: **smart_defense.py** and **container_defense.py**
- Run the **smart_defense.py** when launching an attack on the VM, and **container_defense.py** when launching an attack on the container
- Before running any of the defense script, please go into each script and edit the CONTAINER_NAME and ATTACKER_IP to your own container's name and your **Attacker VM**'s name
cd target_vm/defense
sudo python3 smart_defense.py **or**
sudo python3 container_defense.py

### 4. Launch Network-based attacks from Attacker VM
- Remember to launch each attach individualy and not together
- After each attack, remember to run "sudo iptables -F" to reset the firewall rules so that other attacks can be test appropriately
- SYN Flood Attack:
    cd Cloud-Security-Project/attacker_vm
    sudo bash syn_flood_vm.sh <Target_VM_IP>
- UDP Flood Attack:
    cd Cloud-Security-Project/attacker_vm
    sudo bash udp_flood.sh <Target_VM_IP>

### 4. Launch Host-based attacks from Target VM
- Remember to launch each attach individualy and not together
- After each attack, remember to run "sudo iptables -F" to reset the firewall rules so that other attacks can be test appropriately
- CPU and Memory Bomb Attack:
    cd Cloud-security-Project/target_vm/host-attack
    sudo bash cpu_memory_bomb.sh
- CPU Stress attack (inside the container):
    
### (Optional) 5. Generate a Resource Usage Graph for each attack
- After each attack, there's two available scripts to generate a resource usage graph for the VM and container
    cd Cloud-Security-Project/target_vm/report
    sudo python3 resource_plot.py **or**
    sudo python3 container_resource_plot.py

