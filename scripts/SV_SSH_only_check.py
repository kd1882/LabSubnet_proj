#!/usr/bin/env python3
import socket

TARGETS = {
    "pi5-bastion-01": ("192.168.20.10", 22),
    "pi5-ctrl-01": ("192.168.20.11", 22),
}

def ssh_banner(ip: str, port: int = 22, timeout: float = 2.0) -> str | None:
    try:
        with socket.create_connection((ip, port), timeout=timeout) as s:
            s.settimeout(timeout)
            data = s.recv(128)
        banner = data.decode(errors="ignore").strip()
        return banner if banner.startswith("SSH-") else banner
    except Exception:
        return None

def main() -> None:
    for name, (ip, port) in TARGETS.items():
        banner = ssh_banner(ip, port)
        if banner:
            print(f"{name} ({ip}:{port}) banner: {banner}")
        else:
            print(f"{name} ({ip}:{port}) unreachable or no banner")

if __name__ == "__main__":
    main()
