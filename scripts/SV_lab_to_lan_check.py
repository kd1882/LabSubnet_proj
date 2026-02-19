#!/usr/bin/env python3
import socket

HOME_LAN_TESTS = [
    ("AXE95", "192.168.1.1", 80),
    ("AXE95-DNS?", "192.168.1.1", 53),
]

def tcp_probe(ip: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except Exception:
        return False

def main() -> None:
    print("Lab Node → Home LAN egress test (expected: BLOCKED)\n")
    for name, ip, port in HOME_LAN_TESTS:
        ok = tcp_probe(ip, port)
        print(f"{name:10} {ip:15} tcp/{port:<4} {'UNEXPECTED OPEN' if ok else 'BLOCKED (expected)'}")

if __name__ == "__main__":
    main()
