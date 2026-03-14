"""
Port scanning logic using threading for speed.
"""

import socket
import concurrent.futures
from typing import List, Dict


# Common service names for well-known ports
COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 5432: "PostgreSQL",
    6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB",
}


class PortScanner:
    def __init__(self, timeout: float = 0.5, max_threads: int = 100):
        self.timeout = timeout
        self.max_threads = max_threads

    def _check_port(self, host: str, port: int) -> Dict:
        """Attempt to connect to a single port and return result."""
        result = {"port": port, "open": False, "service": COMMON_SERVICES.get(port, "unknown"), "banner": ""}
        try:
            with socket.create_connection((host, port), timeout=self.timeout) as sock:
                result["open"] = True
                # Try to grab a banner
                try:
                    sock.settimeout(0.2)
                    banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
                    result["banner"] = banner[:80]
                except Exception:
                    pass
        except (socket.timeout, ConnectionRefusedError, OSError):
            pass
        return result

    def _parse_ports(self, port_str: str) -> List[int]:
        """Parse port string like '22,80,443' or '1-1024'."""
        ports = []
        for part in port_str.split(","):
            part = part.strip()
            if "-" in part:
                start, end = part.split("-")
                ports.extend(range(int(start), int(end) + 1))
            else:
                ports.append(int(part))
        return sorted(set(ports))

    def scan(self, host: str, port_str: str) -> List[Dict]:
        """Scan all specified ports on the given host."""
        # Resolve hostname first
        try:
            ip = socket.gethostbyname(host)
        except socket.gaierror as e:
            raise ValueError(f"Cannot resolve host '{host}': {e}")

        ports = self._parse_ports(port_str)
        open_ports = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {executor.submit(self._check_port, ip, p): p for p in ports}
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result["open"]:
                    open_ports.append(result)
                    print(f"  [OPEN] Port {result['port']:5d}/tcp  {result['service']}")

        return sorted(open_ports, key=lambda x: x["port"])
