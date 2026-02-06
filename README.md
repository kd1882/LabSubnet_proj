# Overview

Project Intent - Set up a subnet off of my LAN that restricts access to assets within the subnet - starting off simple with vlan segmentation then growing the capability with the end goal of having a subnet that is accessed through a bastion host -> subnet has 802.1x implemented -> bastion host can only be accessed by whitelisted assets with MFA from trusted lan (growing to VPN into trusted lan with MFA). Currently waiting on dual nic hat for the rpi5-16 so moving ahead with vlan segmentation.

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

Additional project information in the docs folder as to progress/updates/config changes.
