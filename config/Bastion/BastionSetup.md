# Bastion Host Setup Documentation

## Purpose

The Bastion host serves as the sole administrative access point into the segmented lab enclave (192.168.20.0/24).

All access to Kubernetes control plane and worker nodes is mediated through this system. Direct access from the Home LAN into lab assets is explicitly denied at the boundary firewall.

This host functions as:

* SSH jump host
* Kubernetes administrative node
* Controlled access broker
* Logging and audit enforcement point

It is not configured to route traffic, host workloads, or provide general-purpose services.

---

# System Information

* Platform: Raspberry Pi 5 (16GB)
* OS: Raspberry Pi OS Lite (64-bit)
* Hostname: `bastion`
* Static IP: `192.168.20.10`
* Gateway: `192.168.20.1` (OpenWrt boundary firewall)

---

# Network Configuration

The Bastion is single-homed on the lab subnet.

### Static IP Configuration

`/etc/dhcpcd.conf`

```bash
interface eth0
static ip_address=192.168.20.10/24
static routers=192.168.20.1
static domain_name_servers=192.168.20.1
```

Reboot after configuration:

```bash
sudo reboot
```

---

# Routing Controls

IP forwarding is disabled to prevent accidental routing between networks.

### Disable IP Forwarding (Runtime)

```bash
sudo sysctl -w net.ipv4.ip_forward=0
```

### Persist Setting

`/etc/sysctl.conf`

```bash
net.ipv4.ip_forward=0
```

Verification:

```bash
sysctl net.ipv4.ip_forward
```

Expected output:

```bash
net.ipv4.ip_forward = 0
```

---

# Boundary Firewall Configuration (OpenWrt)

On the Archer A7 (OpenWrt):

### Allow Rule

* Source: Home LAN (192.168.1.0/24)
* Destination: 192.168.20.10
* Protocol: TCP
* Port: 22
* Action: Allow

### Explicit Deny

* Home LAN → 192.168.20.0/24 (all other traffic)
* Lab subnet → WAN (if egress containment desired)

This ensures the Bastion is the only exposed entry point into the lab enclave.

---

# SSH Hardening

File: `/etc/ssh/sshd_config`

```bash
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers adminuser
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
```

Restart SSH:

```bash
sudo systemctl restart ssh
```

Access is restricted to key-based authentication only.

---

# Required Tooling Installed

The Bastion contains only administrative and monitoring tooling.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
    kubectl \
    git \
    tmux \
    htop \
    jq \
    nmap \
    fail2ban \
    auditd \
    ufw \
    unattended-upgrades
```

The Bastion does not run:

* k3s
* Docker
* Application workloads
* Public services

---

# Kubernetes Administration Setup

The kubeconfig from the control-plane node is copied to the Bastion.

On control plane:

```bash
sudo cat /etc/rancher/k3s/k3s.yaml
```

Copied to Bastion:

```bash
mkdir -p ~/.kube
nano ~/.kube/config
chmod 600 ~/.kube/config
```

Modify server address:

```yaml
server: https://192.168.20.11:6443
```

Verification:

```bash
kubectl get nodes
```

Expected output includes:

* pi5-ctrl-01
* pi5-worker-01
* pi5-worker-02
* pi5-worker-03

The Bastion is now the cluster administration node.

---

# SSH Jump Configuration (Client-Side)

On the administrative laptop:

`~/.ssh/config`

```bash
Host bastion
    HostName 192.168.20.10
    User adminuser
    IdentityFile ~/.ssh/id_ed25519

Host pi5-*
    ProxyJump bastion
    User pi
    IdentityFile ~/.ssh/id_ed25519
```

This enables transparent proxying:

```bash
ssh pi5-ctrl-01
```

All access is mediated through the Bastion.

---

# Logging and Intrusion Protection

### Enable Fail2Ban

```bash
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Enable AuditD

```bash
sudo systemctl enable auditd
sudo systemctl start auditd
```

### UFW Baseline (Optional)

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw enable
```

---

# Security Posture

The Bastion enforces:

* No password-based authentication
* No root login
* No routing functionality
* No internet exposure
* No direct IT → OT connectivity
* No workload hosting

It operates as a hardened, minimal administrative access broker.

---

# Access Model Summary

Permitted:

* Home LAN → Bastion (SSH only)
* Bastion → k3s Nodes (SSH / API)

Denied:

* Home LAN → k3s Nodes (direct)
* Lab Subnet → Home LAN
* Lab Subnet → Internet (if egress blocked)

This enforces a mediated access pattern consistent with segmented enclave architecture.

---

# Future Enhancements

Planned improvements:

* SSH MFA enforcement
* Centralized logging aggregation
* VLAN-based separation (Mgmt vs Workload)
* IDS within enclave
* Immutable bastion image rebuild process

---

This Bastion implementation provides a controlled administrative boundary for the Kubernetes lab cluster while maintaining strict segmentation from the primary home LAN.
