#!/usr/bin/env bash
set -euo pipefail

BASTION_IP="${BASTION_IP:-192.168.20.10}"
BASTION_USER="${BASTION_USER:-adminuser}"
NODE_USER="${NODE_USER:-pi}"
IDENTITY_FILE="${IDENTITY_FILE:-~/.ssh/id_ed25519}"

cat <<EOF
# --- Bastion + k3s node access ---
Host bastion
  HostName ${BASTION_IP}
  User ${BASTION_USER}
  IdentityFile ${IDENTITY_FILE}
  IdentitiesOnly yes

Host pi5-ctrl-01 pi5-worker-01 pi5-worker-02 pi5-worker-03
  User ${NODE_USER}
  IdentityFile ${IDENTITY_FILE}
  IdentitiesOnly yes
  ProxyJump bastion
EOF
