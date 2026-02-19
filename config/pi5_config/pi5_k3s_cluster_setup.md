# Lab Cluster Build Documentation

Subnet: **192.168.20.0/24**

---

# 1. Node Inventory

| Hostname       | IP            | Hardware | Role              |
| -------------- | ------------- | -------- | ----------------- |
| pi5-bastion-01 | 192.168.20.10 | Pi5 16GB | SSH Gateway       |
| pi5-ctrl-01    | 192.168.20.11 | Pi5 8GB  | k3s Control Plane |
| pi5-worker-01  | 192.168.20.21 | Pi5 8GB  | k3s Agent         |
| pi5-worker-02  | 192.168.20.22 | Pi5 8GB  | k3s Agent         |
| pi5-worker-03  | 192.168.20.23 | Pi5 8GB  | k3s Agent         |
| pi4-rancher-01 | 192.168.20.30 | Pi4      | Rancher / Utility |

---

# 2. Imaging Standard

## OS

**Raspberry Pi OS Lite (64-bit)**
GUI only used temporarily for troubleshooting NVMe if needed.

## Raspberry Pi Imager Settings

* Hostname: Set per table above
* Username: `admin` (or standardized lab admin)
* Password: strong password (temporary if using SSH keys)
* SSH: Enabled
* WiFi: Enabled for initial setup only
* Timezone: Eastern
* Keyboard: US
* Telemetry: Disabled

After provisioning, disable WiFi if using wired-only segmentation.

---

# 3. Base OS Preparation (All Pi5 Nodes)

### Update System

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y vim curl
```

---

# 4. NVMe Enablement (Pi5 Nodes)

### Enable PCIe

Edit:

```bash
sudo vim /boot/firmware/config.txt
```

Add:

```
dtparam=pciex1
```

Reboot:

```bash
sudo reboot
```

Verify:

```bash
lspci
```

NVMe controller should appear.

---

### Set Boot Order to NVMe

```bash
sudo raspi-config
```

Advanced Options → Boot Order → NVMe First

If prompted regarding EEPROM update, approve latest version.

---

# 5. Enable cgroups (Required for k3s)

Edit:

```bash
sudo vim /boot/firmware/cmdline.txt
```

Append to the single existing line:

```
cgroup_memory=1 cgroup_enable=memory
```

Reboot.

Verify:

```bash
cat /proc/cmdline
```

---

# 6. Hostname Configuration

On each node:

```bash
sudo hostnamectl set-hostname <hostname>
```

Example:

```bash
sudo hostnamectl set-hostname pi5-worker-01
```

Update `/etc/hosts` on all nodes:

```
192.168.20.10 pi5-bastion-01
192.168.20.11 pi5-ctrl-01
192.168.20.21 pi5-worker-01
192.168.20.22 pi5-worker-02
192.168.20.23 pi5-worker-03
192.168.20.30 pi4-rancher-01
```

Reboot after changes.

---

# 7. k3s Installation

## Control Plane (pi5-ctrl-01)

```bash
curl -sfL https://get.k3s.io | sh -
```

Verify:

```bash
sudo kubectl get nodes
```

Retrieve cluster token:

```bash
sudo cat /var/lib/rancher/k3s/server/node-token
```

---

## Worker Nodes (pi5-worker-01/02/03)

```bash
curl -sfL https://get.k3s.io | \
K3S_URL=https://192.168.20.11:6443 \
K3S_TOKEN=<server-token> sh -
```

Verify from control plane:

```bash
sudo kubectl get nodes
```

All nodes should report `Ready`.

---

# 8. Rancher Deployment (pi4-rancher-01)

Install Docker:

```bash
curl -fsSL https://get.docker.com | sh
```

Deploy Rancher:

```bash
docker run -d --restart=unless-stopped \
-p 80:80 -p 443:443 \
--privileged \
rancher/rancher:latest
```

Access:

```
https://192.168.20.30
```

Import existing k3s cluster via Rancher UI.

---

# 9. Bastion Host (pi5-bastion-01)

Purpose: Single ingress point into 192.168.20.0/24 subnet.

Minimum baseline:

* Disable password SSH login
* Enforce SSH key authentication
* Restrict inbound firewall rules to admin workstation IP only
* No k3s workloads hosted here

Example SSH hardening:

Edit `/etc/ssh/sshd_config`:

```
PasswordAuthentication no
PermitRootLogin no
```

Restart SSH:

```bash
sudo systemctl restart ssh
```

---

# 10. Known Issues / Lessons Learned

### USB Boot

USB media causes significant latency and slow cluster initialization.
Not recommended for cluster nodes.

### cgroup Misconfiguration

If pods fail to start:

* Verify cgroup flags exist in `/proc/cmdline`
* Reboot if missing

### Token Errors

* Confirm control plane IP (192.168.20.11)
* Confirm port 6443 reachable
* Ensure token copied exactly

---

# 11. Validation Checklist

* [ ] All nodes on 192.168.20.0/24
* [ ] Hostnames match inventory table
* [ ] NVMe detected (Pi5 nodes)
* [ ] Boot order set correctly
* [ ] cgroups enabled
* [ ] k3s control plane operational
* [ ] Workers joined and Ready
* [ ] Rancher accessible
* [ ] Bastion hardened
* [ ] WiFi disabled on cluster nodes (if not required)
