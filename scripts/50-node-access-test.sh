#!/usr/bin/env bash
set -euo pipefail

NODES=(
  "192.168.20.11"
  "192.168.20.21"
  "192.168.20.22"
  "192.168.20.23"
)

echo "[*] Testing TCP/22 reachability to k3s nodes..."
for ip in "${NODES[@]}"; do
  if timeout 2 bash -c "cat < /dev/null > /dev/tcp/${ip}/22" 2>/dev/null; then
    echo "OK   ${ip}:22"
  else
    echo "FAIL ${ip}:22"
  fi
done
