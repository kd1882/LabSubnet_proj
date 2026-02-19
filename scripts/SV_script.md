# SV How-To

### SV?
Security Verification, simple python scripts to check network/system hardening.

## Suggested run pattern (what to run where)

### Admin Laptop (192.168.1.x):

- SV_boundary_verification.py - Checks whether ports are reachable on each lab IP and prints PASS/FAIL aligned to your policy.

- SV_SSH_only_check.py - validates that TCP/22 is reachable and that the remote is actually speaking SSH (not just an open port). Run from Home LAN.

### pi5-bastion-01 (192.168.20.10):

- SV_bastion_to_node_check.py - Confirms you can reach SSH to nodes and the k3s API.

- SV_bastion_config_audit.py - Checks common hardening items: SSH password disabled, forwarding off, fail2ban/auditd presence.

### pi5-worker-0x / pi5-ctrl-01:

- SV_lab_to_lan_check.py - Checks that Home LAN addresses aren’t reachable (ICMP + TCP).