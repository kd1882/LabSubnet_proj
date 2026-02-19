#!/usr/bin/env python3
import socket
from dataclasses import dataclass
from typing import Dict, List, Tuple

TIMEOUT = 1.0

@dataclass(frozen=True)
class Host:
    name: str
    ip: str

HOSTS: List[Host] = [
    Host("pi5-bastion-01", "192.168.20.10"),
    Host("pi5-ctrl-01", "192.168.20.11"),
    Host("pi5-worker-01", "192.168.20.21"),
    Host("pi5-worker-02", "192.168.20.22"),
    Host("pi5-worker-03", "192.168.20.23"),
    Host("pi4-rancher-01", "192.168.20.30"),
]

# Expected policy from HOME LAN perspective:
# - Only bastion should have TCP/22 reachable
# - Everything else should be unreachable on TCP/22 (and optionally 443/80/6443)
EXPECTED_OPEN: Dict[Tuple[str, int], bool] = {
    ("192.168.20.10", 22): True,   # bastion SSH allowed
}

PORTS_TO_TEST = [22, 80, 443, 6443]  # add/remove depending on what you want to validate

def can_connect(ip: str, port: int, timeout: float = TIMEOUT) -> bool:
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except Exception:
        return False

def expected(ip: str, port: int) -> bool:
    return EXPECTED_OPEN.get((ip, port), False)

def main() -> None:
    print("Home LAN → Lab Subnet reachability test (expected: ONLY bastion:22 reachable)\n")
    failures = 0

    for h in HOSTS:
        for port in PORTS_TO_TEST:
            actual = can_connect(h.ip, port)
            exp = expected(h.ip, port)
            status = "PASS" if actual == exp else "FAIL"
            if status == "FAIL":
                failures += 1
            print(f"{status:4}  {h.name:14} {h.ip:15} tcp/{port:<4} actual={'OPEN' if actual else 'CLOSED'} expected={'OPEN' if exp else 'CLOSED'}")

    print("\nSummary:", "OK" if failures == 0 else f"{failures} failure(s)")
    raise SystemExit(0 if failures == 0 else 2)

if __name__ == "__main__":
    main()
