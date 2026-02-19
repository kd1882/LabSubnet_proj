# Network Segmentation Lab – Bastion-Mediated Enclave

## Overview

This project implements a segmented lab subnet behind a primary home LAN to demonstrate:

* Layer 3 network segmentation
* Firewall-based boundary enforcement
* Bastion-mediated administrative access
* Controlled IT → OT access patterns
* Kubernetes cluster isolation
* Least-privilege routing and traffic flow control

The lab network is treated as a logically isolated enclave accessible only through a hardened bastion host.

---

# Architecture Summary

## Primary Edge Router

**TP-Link Archer AXE95**

* 192.168.1.1/24
* Home LAN gateway

## Lab Boundary Firewall

**TP-Link Archer A7 (OpenWrt)**

* WAN: 192.168.1.2
* LAN: 192.168.20.1/24
* Functions as segmented enclave firewall

## Lab Distribution Switch

**TP-Link TL-SG106PME**

* Layer 2 distribution for lab subnet
* No routing functionality

---

# Network Topology

```
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
pi5-bastion-01 (192.168.20.10)
        ↓
k3s Cluster Nodes
```

The Archer A7 acts as the Layer 3 security boundary.
`pi5-bastion-01` acts as the authenticated access broker.

There is **no direct routing from the Home LAN into the lab subnet.**

---

# Lab Subnet

Subnet: **192.168.20.0/24**
Gateway: **192.168.20.1 (OpenWrt)**

| Hostname       | IP            | Role               |
| -------------- | ------------- | ------------------ |
| pi5-bastion-01 | 192.168.20.10 | SSH Access Gateway |
| pi5-ctrl-01    | 192.168.20.11 | k3s Control Plane  |
| pi5-worker-01  | 192.168.20.21 | k3s Agent          |
| pi5-worker-02  | 192.168.20.22 | k3s Agent          |
| pi5-worker-03  | 192.168.20.23 | k3s Agent          |
| pi4-rancher-01 | 192.168.20.30 | Rancher / Utility  |

---

# k3s Cluster Architecture

```
k3s Cluster (192.168.20.0/24)
--------------------------------

Control Plane:
  pi5-ctrl-01
  - k3s server
  - API Server
  - Scheduler
  - Embedded datastore (etcd)

Worker Nodes:
  pi5-worker-01
  pi5-worker-02
  pi5-worker-03
```

Cluster administration is performed exclusively from `pi5-bastion-01` using `kubectl`.

The Bastion contains the kubeconfig and is the only system authorized to communicate directly with the control plane API.

---

# Access Control Model

## Administrative Access Flow

```
Admin Laptop (192.168.1.x)
    ↓
AXE95
    ↓
Archer A7 (Firewall rule: allow SSH to bastion only)
    ↓
pi5-bastion-01 (192.168.20.10)
    ↓
SSH to cluster nodes
    ↓
kubectl to control plane
```

No cluster node is directly accessible from the Home LAN.

---

# Policy Enforcement

The OpenWrt firewall enforces explicit deny rules.

### Blocked Traffic

* Home LAN → pi5-ctrl-01 ❌
* Home LAN → pi5-worker-* ❌
* Home LAN → Lab Subnet ❌ (except bastion SSH)
* pi5-worker-* → Internet ❌ (egress restricted)
* pi5-worker-* → Home LAN ❌

### Allowed Traffic

* Home LAN → pi5-bastion-01 (TCP/22 only)
* pi5-bastion-01 → pi5-ctrl-01 (API / SSH as required)
* pi5-bastion-01 → pi5-worker-* (SSH as required)
* pi5-ctrl-01 ↔ pi5-worker-* (k3s cluster communication)

This enforces strict IT → OT mediation.

---

# Bastion Host Configuration

`pi5-bastion-01` is configured with:

* Static IP (192.168.20.10)
* IP forwarding disabled
* SSH key-based authentication only
* Password authentication disabled
* Fail2ban enabled
* auditd enabled
* No container workloads
* No public exposure
* No routing capability

It functions strictly as:

* SSH jump host
* Kubernetes administrative node
* Controlled access broker into enclave

---

# Security Objectives Demonstrated

This lab demonstrates:

* Segmented enclave architecture
* Centralized boundary enforcement
* Bastion-mediated access control
* Least privilege traffic flow
* North-South vs East-West filtering
* Control plane isolation
* Kubernetes workload containment
* Defense-in-depth implementation at small scale
