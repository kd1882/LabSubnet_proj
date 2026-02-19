#!/usr/bin/env bash
set -euo pipefail

SUBNET="${1:-192.168.20.0/24}"

echo "[*] Discovering live hosts on ${SUBNET}..."
sudo nmap -sn "${SUBNET}" -oG - | awk '/Up$/{print $2}' | sort
