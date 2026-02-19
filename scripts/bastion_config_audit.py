#!/usr/bin/env python3
import os
import re
import subprocess
from pathlib import Path

def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return p.returncode, p.stdout.strip()

def check_sshd_config() -> list[str]:
    findings = []
    cfg = Path("/etc/ssh/sshd_config")
    if not cfg.exists():
        return ["sshd_config not found"]

    text = cfg.read_text(errors="ignore")
    def get(setting: str) -> str | None:
        m = re.search(rf"(?im)^\s*{re.escape(setting)}\s+(\S+)\s*$", text)
        return m.group(1) if m else None

    pw = get("PasswordAuthentication")
    root = get("PermitRootLogin")
    if pw is None or pw.lower() != "no":
        findings.append(f"SSH: PasswordAuthentication is not 'no' (found: {pw})")
    if root is None or root.lower() not in {"no", "prohibit-password"}:
        findings.append(f"SSH: PermitRootLogin not hardened (found: {root})")
    return findings

def check_ip_forwarding() -> list[str]:
    findings = []
    paths = ["/proc/sys/net/ipv4/ip_forward", "/proc/sys/net/ipv6/conf/all/forwarding"]
    for p in paths:
        try:
            v = Path(p).read_text().strip()
            if v != "0":
                findings.append(f"Forwarding enabled: {p}={v} (expected 0)")
        except Exception as e:
            findings.append(f"Could not read {p}: {e}")
    return findings

def check_service_active(name: str) -> str | None:
    rc, out = run(["systemctl", "is-active", name])
    return None if (rc == 0 and out == "active") else f"Service {name} not active (state: {out})"

def check_package_installed(binary: str) -> str | None:
    rc, _ = run(["bash", "-lc", f"command -v {binary}"])
    return None if rc == 0 else f"Binary '{binary}' not found"

def main() -> None:
    findings: list[str] = []

    findings += check_sshd_config()
    findings += check_ip_forwarding()

    # fail2ban + auditd checks (service name can vary slightly by distro)
    for svc in ["fail2ban", "auditd"]:
        msg = check_service_active(svc)
        if msg:
            findings.append(msg)

    # basic binaries
    for binname in ["sshd", "iptables", "nft", "journalctl"]:
        msg = check_package_installed(binname)
        if msg:
            findings.append(msg)

    if findings:
        print("HARDENING CHECK: FAIL\n")
        for f in findings:
            print(f"- {f}")
        raise SystemExit(2)
    else:
        print("HARDENING CHECK: PASS")

if __name__ == "__main__":
    main()
