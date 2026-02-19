#!/usr/bin/env bash
set -euo pipefail

BASTION_USER="${BASTION_USER:-adminuser}"

if [[ $EUID -ne 0 ]]; then
  echo "ERROR: run as root (sudo)"
  exit 1
fi

echo "[*] Disabling IP forwarding..."
sysctl -w net.ipv4.ip_forward=0 >/dev/null
grep -q '^net.ipv4.ip_forward=0' /etc/sysctl.conf || echo 'net.ipv4.ip_forward=0' >> /etc/sysctl.conf

echo "[*] Creating SSH hardening drop-in..."
install -d -m 0755 /etc/ssh/sshd_config.d

cat >/etc/ssh/sshd_config.d/10-bastion-hardening.conf <<EOF
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
ChallengeResponseAuthentication no
PubkeyAuthentication yes
AllowUsers ${BASTION_USER}
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
X11Forwarding no
AllowTcpForwarding no
PermitTunnel no
EOF

echo "[*] Validating sshd config..."
sshd -t

echo "[*] Configuring UFW..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp comment "SSH to bastion"
ufw --force enable

echo "[*] Restarting ssh..."
systemctl restart ssh

echo "[*] Hardening complete."
echo "[!] Reminder: ensure OpenWrt only allows TCP/22 from Home LAN to this bastion IP."
