#!/usr/bin/env bash
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "ERROR: run as root (sudo)"
  exit 1
fi

echo "[*] Updating system..."
apt-get update -y
apt-get upgrade -y

echo "[*] Installing baseline tooling..."
apt-get install -y \
  git tmux htop jq nmap curl wget ca-certificates gnupg lsb-release \
  fail2ban auditd ufw unattended-upgrades

echo "[*] Enabling services..."
systemctl enable --now fail2ban
systemctl enable --now auditd

echo "[*] Enabling unattended upgrades..."
dpkg-reconfigure -f noninteractive unattended-upgrades || true

echo "[*] Done."
