# 20260209 Update

Going to do some more holistic troubleshooting and root cause analaysis.

- Still unable to ping upstream for lab environment (192.168.20.1)
- DHCP is not pulling/assigning an address for ethernet
- openwrt is showing there is a connection

## Knowns
- Maintenance laptop is not connected to WiFi
- Test laptop is not connected to WiFi
- I have br-lan / br-lab
- 192.168.1.137 is my maint laptop


## Maybe
- disabled ipv6 on port4 for brlab
- took off the firewall for lab, made accept for everything else
- going to rebuild it on port 3...
- went through with the config, set static IP and ping test worked

```bash
# flushing
sudo ip addr flush dev eth0
sudo dhclient -v eth0
```

Noted dhcp pulled from 192.168.1.1 not 192.168.20.1 - port three is still active on br-lan AND br-lab.

Have to review settings and hardware diagram for netgear r7000 more thoroughly before trying to implement this further or just wait until the dual nic hat comes in and properly set it up as a bastion into the subnet.

Currently able to get isolation via policies/firewalls on L3.

*Uploading commands and updated config next nap*

---

Update - should've looked at the docs for openwrt and the ac1900 r7000. Broadcom chipsets are not FOSS friendly at all with limited support and functionality.
- Confirmed this was the issue with limited functionality with the r7000.

---

Pulled R7000 from config, flashed Archer A7 ac1750 ver 5.0 with openwrt, still need to do diagrams and configs, dual hat nic comes in tomorrow. 

WAN -> Modem -> Router (home Lan) -> Bastion Host -> Router (lab Lan)

