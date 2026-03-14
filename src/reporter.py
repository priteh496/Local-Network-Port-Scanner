"""
Formats and outputs scan results.
"""

from typing import List, Dict
from datetime import datetime


class Reporter:
    def __init__(self, target: str, results: List[Dict]):
        self.target = target
        self.results = results
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def print_summary(self):
        print("\n" + "=" * 55)
        print(f"  Scan Report — {self.target}  [{self.timestamp}]")
        print("=" * 55)
        if not self.results:
            print("  No open ports found.")
        else:
            print(f"  {'PORT':<10} {'SERVICE':<15} {'BANNER'}")
            print("  " + "-" * 53)
            for r in self.results:
                banner = r["banner"][:35] if r["banner"] else ""
                print(f"  {r['port']:<10} {r['service']:<15} {banner}")
        print(f"\n  Total open: {len(self.results)}")
        print("=" * 55)

    def save(self, filepath: str):
        lines = [
            f"Port Scan Report",
            f"Target : {self.target}",
            f"Date   : {self.timestamp}",
            f"Open   : {len(self.results)}",
            "-" * 50,
        ]
        for r in self.results:
            lines.append(f"{r['port']}/tcp  {r['service']}  {r['banner']}")
        with open(filepath, "w") as f:
            f.write("\n".join(lines))
