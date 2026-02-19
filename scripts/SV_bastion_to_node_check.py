#!/usr/bin/env python3
import socket
from dataclasses import dataclass

TIMEOUT = 1.0

@dataclass(frozen=True)
class Target:
    name: str
    ip: str

NODES = [
    Target("pi5-ctrl-01", "192.168.20.11"),
    Target("pi5-worker-01", "192.168.20.21"),
    Target("pi5-worker-02", "192.168.20.22"),
    Target("pi5-worker-03", "192.168.20.23"),
    Target("pi4-rancher-01", "192.168.20.30"),
]

PORTS = [22, 6443, 443]

def can_connect(ip: str, port: int) -> bool:
    try:
        with socket.create_connection((ip, port), timeout=TIMEOUT):
            return True
    except Exception:
        return False

def main() -> None:
    print("Bastion → Lab internal connectivity\n")
    for t in NODES:
        for p in PORTS:
            ok = can_connect(t.ip, p)
            print(f"{'OK' if ok else 'NO'}  {t.name:14} {t.ip:15} tcp/{p}")
        print()

if __name__ == "__main__":
    main()
