# Network Segmentation Lab – Bastion-Mediated Enclave

## Overview

This project implements a segmented lab subnet behind my primary home LAN in order to demonstrate:

* Layer 3 network segmentation
* Firewall-based boundary enforcement
* Bastion-mediated administrative access
* Controlled IT → OT access patterns
* Kubernetes cluster isolation
* Least-privilege routing and traffic flow control

The lab network is treated as an isolated enclave accessible only through a hardened bastion host.

---

## Architecture Summary

Primary edge router:

* TP-Link Archer AXE95

  * 192.168.1.1/24
  * Home LAN gateway

Lab boundary firewall:

* TP-Link Archer A7 running OpenWrt

  * WAN: 192.168.1.2
  * LAN: 192.168.20.1/24
  * Functions as segmented enclave firewall

Lab switch:

* TP-Link TL-SG106PME

  * Layer 2 distribution for lab subnet

---

## Network Topology

```text
Admin Laptop (192.168.1.x)
        ↓
AXE95 (192.168.1.1)
        ↓
Archer A7 (OpenWrt Firewall)
WAN: 192.168.1.2
LAN: 192.168.20.1
        ↓
Lab Switch (192.168.20.0/24)
        ↓
Bastion (192.168.20.10)
        ↓
k3s Cluster Nodes
```

The Archer A7 acts as the security boundary.
The Bastion acts as the authenticated access broker.

There is no direct routing from Home LAN into the lab subnet.

---

## Lab Subnet

**Subnet:** 192.168.20.0/24
**Gateway:** 192.168.20.1 (OpenWrt)

| Device        | IP            | Role               |
| ------------- | ------------- | ------------------ |
| Bastion       | 192.168.20.10 | SSH Access Gateway |
| pi5-ctrl-01   | 192.168.20.11 | k3s Control Plane  |
| pi5-worker-01 | 192.168.20.21 | k3s Agent          |
| pi5-worker-02 | 192.168.20.22 | k3s Agent          |
| pi5-worker-03 | 192.168.20.23 | k3s Agent          |

---

## k3s Cluster Architecture

```text
k3s Cluster (192.168.20.0/24)
--------------------------------

Control Plane:
  pi5-ctrl-01
  - k3s server
  - API Server
  - Scheduler
  - etcd

Worker Nodes:
  pi5-worker-01 (agent)
  pi5-worker-02 (agent)
  pi5-worker-03 (agent)
```

Cluster administration is performed from the Bastion host using `kubectl`.

The Bastion contains the kubeconfig and is the only system authorized to communicate directly with the control plane API.

---

## Access Control Model

Administrative access flow:

```text
Admin Laptop (192.168.1.x)
    ↓
AXE95
    ↓
Archer A7 (firewall rule: allow SSH to bastion only)
    ↓
Bastion (192.168.20.10)
    ↓
SSH to pi5 nodes
    ↓
kubectl to cluster
```

---

## Policy Enforcement

The OpenWrt firewall enforces explicit deny rules.

```text
Home LAN  → k3s Node      ❌ BLOCKED
Home LAN  → Lab Subnet    ❌ BLOCKED (except Bastion SSH)
k3s Node  → Internet      ❌ BLOCKED (egress restricted)
k3s Node  → Home LAN      ❌ BLOCKED
```

Allowed traffic:

```text
Home LAN → Bastion (TCP/22)
Bastion → k3s Nodes (SSH / API as required)
```

This prevents direct IT → OT communication and enforces access mediation.

---

## Bastion Host Configuration

The Bastion host:

* Static IP on 192.168.20.0/24
* IP forwarding disabled
* SSH key-based authentication only
* Password authentication disabled
* Fail2ban enabled
* auditd enabled
* No container workloads
* No external exposure

It functions strictly as:

* SSH jump host
* Kubernetes administrative node
* Controlled access broker into enclave

---

## Security Objectives Demonstrated

This lab demonstrates:

* Segmented enclave architecture
* Centralized boundary enforcement
* Bastion-mediated access control
* Least privilege traffic flow
* North-South vs East-West filtering
* Control plane isolation
* Kubernetes cluster containment
* Defense-in-depth at small scale

---

## Current Status

* Dual-router segmentation implemented
* OpenWrt boundary firewall configured
* Lab subnet isolated (192.168.20.0/24)
* Bastion hardened and operational
* k3s cluster deployed and reachable only via bastion
* Direct Home LAN → Lab access blocked

---

## Future Enhancements

* VLAN-based internal separation (Mgmt vs Workload plane)
* Logging aggregation and centralized monitoring
* MFA-enabled SSH on Bastion
* HA control plane expansion
* IDS/IPS within lab boundary
* Network policy enforcement within Kubernetes

---

Additional documentation, configuration snapshots, and updates are located in the `/docs` directory.
