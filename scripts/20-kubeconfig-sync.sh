#!/usr/bin/env bash
set -euo pipefail

CTRL_HOST="${CTRL_HOST:-192.168.20.11}"
CTRL_USER="${CTRL_USER:-pi}"
KUBECONFIG_DST="${KUBECONFIG_DST:-$HOME/.kube/config}"
K3S_YAML_PATH="${K3S_YAML_PATH:-/etc/rancher/k3s/k3s.yaml}"
API_SERVER_URL="${API_SERVER_URL:-https://192.168.20.11:6443}"

echo "[*] Creating kube dir..."
mkdir -p "$(dirname "$KUBECONFIG_DST")"
chmod 700 "$(dirname "$KUBECONFIG_DST")"

echo "[*] Pulling kubeconfig from control plane ${CTRL_USER}@${CTRL_HOST}..."
# Needs passwordless sudo on control plane for this command or use root login over SSH (not recommended).
ssh "${CTRL_USER}@${CTRL_HOST}" "sudo cat '${K3S_YAML_PATH}'" > "${KUBECONFIG_DST}.tmp"

echo "[*] Rewriting server endpoint to ${API_SERVER_URL}..."
# Replace the default 127.0.0.1 server reference
sed -i "s#https://127.0.0.1:6443#${API_SERVER_URL}#g" "${KUBECONFIG_DST}.tmp"

mv "${KUBECONFIG_DST}.tmp" "${KUBECONFIG_DST}"
chmod 600 "${KUBECONFIG_DST}"

echo "[*] Testing kubectl connectivity..."
KUBECONFIG="${KUBECONFIG_DST}" kubectl get nodes -o wide
echo "[*] Done."
