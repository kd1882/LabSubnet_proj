# Archer A7 (OpenWrt) – Lab Boundary Firewall Configuration

**Role:** Segmented Enclave Firewall
**Model:** TP-Link Archer A7
**Firmware:** OpenWrt
**WAN:** 192.168.1.2
**LAN:** 192.168.20.1/24
**Purpose:** Enforce strict Layer 3 boundary between Home LAN (192.168.1.0/24) and Lab Subnet (192.168.20.0/24)

---

# 1. Architectural Role

The Archer A7 operates as:

* Layer 3 segmentation boundary
* Default gateway for 192.168.20.0/24
* Stateful firewall enforcing explicit deny rules
* Egress restriction point
* Bastion mediation enforcement

It is not used for:

* Wireless access
* DHCP relay into Home LAN
* NAT from Lab → Internet (unless explicitly allowed)

---

# 2. Network Interfaces

## WAN Interface

* Protocol: Static IPv4
* IP: 192.168.1.2
* Gateway: 192.168.1.1 (AXE95)
* DNS: 192.168.1.1 or upstream DNS
* Zone: `wan`

This interface connects to the Home LAN router.

---

## LAN Interface

* Protocol: Static IPv4
* IP: 192.168.20.1
* Netmask: 255.255.255.0
* DHCP: Enabled (optional) or static addressing preferred
* Zone: `lan`

Connected to TL-SG106PME lab switch.

---

# 3. Firewall Zone Model

OpenWrt default zone model modified to enforce enclave posture.

## Zones

### LAN Zone (Lab Subnet)

* Input: REJECT
* Output: ACCEPT
* Forward: REJECT

### WAN Zone (Home LAN Side)

* Input: REJECT
* Output: ACCEPT
* Forward: REJECT
* Masquerading: Disabled (unless controlled egress required)

---

# 4. Required Firewall Rules

## 4.1 Allow SSH from Home LAN to Bastion Only

Allow only:

* Source Zone: WAN
* Source IP: 192.168.1.0/24
* Destination IP: 192.168.20.10 (pi5-bastion-01)
* Protocol: TCP
* Port: 22
* Action: ACCEPT

This rule enables:

Home LAN → pi5-bastion-01 only

No other lab hosts reachable.

---

## 4.2 Block All Other WAN → LAN Traffic

Implicit via default REJECT policy.

Ensure no forwarding rule exists allowing WAN → LAN.

---

## 4.3 Block Lab → Home LAN

Add explicit rule:

* Source Zone: LAN
* Destination Zone: WAN
* Destination IP: 192.168.1.0/24
* Action: REJECT

Prevents:

* pi5-ctrl-01 → Home LAN
* pi5-worker-* → Home LAN

---

## 4.4 Block Lab → Internet (Optional Hard Enclave)

If internet isolation required:

* Disable masquerading on WAN
* No forward rule LAN → WAN

This prevents:

* Container pulls
* Package updates
* External beaconing

If selective egress needed, create host-specific rule for bastion only.

---

# 5. DHCP Configuration (Optional)

If using DHCP:

Range example:

* Start: 192.168.20.100
* Limit: 50
* Lease: 12h

Cluster nodes recommended static:

| Hostname       | IP            |
| -------------- | ------------- |
| pi5-bastion-01 | 192.168.20.10 |
| pi5-ctrl-01    | 192.168.20.11 |
| pi5-worker-01  | 192.168.20.21 |
| pi5-worker-02  | 192.168.20.22 |
| pi5-worker-03  | 192.168.20.23 |
| pi4-rancher-01 | 192.168.20.30 |

Static DHCP reservations recommended for audit consistency.

---

# 6. NAT Strategy

Two deployment modes:

## Mode A – True Enclave (Recommended for Demonstration)

* No NAT
* No LAN → WAN forward
* Bastion-mediated package staging only
* Completely isolated OT environment

Best for segmentation demonstration.

---

## Mode B – Controlled Egress

Allow:

LAN → WAN
Source IP: 192.168.20.10 (bastion only)

Masquerading enabled.

All other lab nodes denied.

---

# 7. Logging & Monitoring

Enable firewall logging for:

* Dropped WAN → LAN attempts
* Blocked LAN → WAN attempts

Navigate:

Network → Firewall → General Settings → Logging

Enable:

* Log dropped packets
* Log rejected packets

Useful for demonstrating boundary enforcement.

---

# 8. Disable Unnecessary Services

On Archer A7:

* Disable/remove WiFi radios/antennas
* Disable UPnP
* Disable WPS
* Disable remote administration
* Restrict LuCI to LAN only
* Change default SSH port (optional)
* Set strong root password

---

# 9. Verification Steps

From Home LAN:

```bash
ssh admin@192.168.20.10
```

Should succeed.

Attempt:

```bash
ssh admin@192.168.20.11
```

Should fail.

From a worker node:

```bash
ping 192.168.1.1
```

Should fail.

From bastion:

```bash
ssh pi5-ctrl-01
kubectl get nodes
```

Should succeed.

---

# 10. Security Posture Summary

This OpenWrt boundary firewall enforces:

* Explicit deny model
* Bastion-mediated access
* No lateral IT → OT movement
* No uncontrolled OT → IT traffic
* Centralized ingress control
* Defense-in-depth at Layer 3