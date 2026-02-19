# 20260206 Update

## Hardware in Use

- Motorola modem
- TP-Link Archer AXE95 (primary home router)
- Netgear Nighthawk AC1900 (R7000)
- TP-Link Archer AC1750 (bridge / AP)
- TP-Link TL-SG106MPE (PoE switch)
- TP-Link TL-SG105E (non-PoE switch)
- Kali Linux laptop (testing)
- System76 PopOS laptop (maintenance)
- Raspberry Pi nodes (not yet connected during testing)

## Intended Roles

- AXE95: Home router (WAN, NAT, DHCP, Wi-Fi)
- R7000 (OpenWrt): Dedicated lab firewall/router
- AC1750 + TP-Link switches: Layer-2 only (no DHCP, no routing)
- Lab network goal:  

- No internet access
- No access to home LAN
- Access only from explicitly allowed LAN hosts (later)

## Firmware State

- R7000 was previously on DD-WRT
- Reflashed successfully to OpenWrt
- OpenWrt LuCI accessible
- Root password set
- Wireless disabled on R7000
- Ethernet-only operation

## OpenWrt UI / Architecture

- Using modern DSA layout
- Menus include:  
	- Network → Interfaces
	- Network → Devices
	- Network → Firewall
- Not using legacy “Switch” page

## Interfaces / Bridges Present

#### The following bridges exist on the R7000:
- br-wan
	- WAN-facing bridge
	- Connected upstream to AXE95
	- Receives DHCP lease in 192.168.1.0/24
- br-lan
	- Management / home-facing bridge
	- IP address: 192.168.1.1
	- Used to access LuCI
	- Port 1 designated as management port
- br-lab
	- Newly created bridge
	- Intended for isolated lab network
	- Interface lab bound to this bridge
	- Static IP: 192.168.20.1/24
	- Gateway: blank
	- DHCP server: enabled

#### Port Intent (Logical)

- Port 1  
	- Intended to remain on br-lan
	- Used for management access to OpenWrt
- Port 4  
	- Intended to be lab uplink
	- Intended to belong to br-lab
	- Kali laptop connected here for testing

## Observed Behavior During Testing

- Kali laptop connected to Port 4
- Interface eth0 showed no IP address
- DHCP client did not receive a lease
- Unable to ping 192.168.20.1
- Indicates traffic from Port 4 was not reaching br-lab

### What Is Confirmed Working

- OpenWrt is functional and accessible
- lab interface exists and is configured
- DHCP server for lab is enabled
- Firewall rules were not the cause of failure
- Issue is isolated to Layer-2 port/bridge association
- No device is bricked
- Configuration changes were paused intentionally

## Current Diagnosis State

- Failure attributed to one or more of:  
	- Physical port numbering mismatch between chassis and LuCI
	- Port 4 not actually attached to br-lab
	- Port 4 still attached to br-lan
	- Bridge not carrying frames to the lab interface

- Further testing deferred until next nap time.

### Updated Logical Diagram (Current State)

```less
                    Internet
                        |
                [ Motorola Modem ]
                        |
              [ TP-Link Archer AXE95 ]
              Home Router / NAT / Wi-Fi
                 192.168.1.0/24
                        |
                 (Ethernet uplink)
                        |
        [ Netgear Nighthawk AC1900 – OpenWrt ]
        ------------------------------------
        | br-wan | br-lan | br-lab          |
        |        |        |                 |
        |        | Port 1 | Port 4 (intended)
        |        | 192.168.1.1              |
        |        |        | 192.168.20.1    |
        ------------------------------------
                        |
               (Layer-2 downstream path)
                        |
              [ Archer AC1750 – bridge ]
                        |
          --------------------------------
          |                              |
   [ TL-SG106MPE ]                [ TL-SG105E ]
      PoE switch                   Non-PoE
      Pi rack                       Pi4 / Pi5

```

  

  

  

  

## Status Summary

- Architecture chosen and validated
- OpenWrt successfully deployed
- Lab interface created but not yet passing traffic
- Work intentionally paused for later continuation

  

  

  

  


