# Overview

Project Intent - Set up a subnet off of my LAN that restricts access to assets within the subnet - starting off simple with vlan segmentation then growing the capability with the end goal of having a subnet that is accessed through a bastion host -> bastion host can be accessed via the trusted LAN -> bastion host can be accessed via VPN with MFA -> subnet supports 802.1x to authenticate clients along with AD for user support.

```less
                        Internet (WAN)
                              |
                           [ Modem ]
                              |
                        ────── LAN ──────
                              |
                    [ Primary Router / Firewall ]
                    (Wi-Fi AP, DHCP, NAT)
                              |
                     ─────────┴─────────
                     |                  |
              [ LAN Clients ]     (Dedicated uplink)
                                     |
                               [ TP-Link Archer ]
                               (Bridge / AP / Switch)
                                     |
                         ────────────┴────────────
                         |                          |
              [ TL-SG106P-ME ]              [ TL-SG105E ]
              (PoE Managed Switch)          (Managed Switch)
                         |                          |
         ┌───────────────┴───────────────┐          |
         |       |       |       |       |          |
     RPi5-8G  RPi5-8G  RPi5-8G  RPi5-8G   (PoE)   RPi4-8G
                                                  RPi5-16G

```

---

## Device Roles

### Edge / Core

- **Modem**
    
    - Pure WAN handoff
        
- **Primary Router**
    
    - NAT, DHCP, firewall
        
    - Wi-Fi for trusted LAN
        
    - _This is your policy enforcement point_
        

### Distribution

- **TP-Link Archer (AC1750)**
    
    - Acts as **Layer-2 bridge / AP / aggregation switch**
        
    - No routing, no DHCP
        
    - Feeds lab switches only
        

### Access / Lab

- **TL-SG106P-ME**
    
    - dumb switch + PoE
        
    - Hosts **4× Raspberry Pi 5 (8GB)**
        
- **TL-SG105E**
    
    - dumb switch (non-PoE)
        
    - Hosts **RPi 4 (8GB)** and **RPi 5 (16GB)**

# LabSubnet_proj
Repo to hold notes, documentation, and configs for a Lab Subnet
