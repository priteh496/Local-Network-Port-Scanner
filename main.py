"""
Local Network Port Scanner
Scans a host or IP range for open TCP ports.
"""

import argparse
from src.scanner import PortScanner
from src.reporter import Reporter


def parse_args():
    parser = argparse.ArgumentParser(description="Local Network Port Scanner")
    parser.add_argument("target", help="IP address or hostname to scan")
    parser.add_argument("-p", "--ports", default="1-1024",
                        help="Port range, e.g. '22,80,443' or '1-1024'")
    parser.add_argument("-t", "--threads", type=int, default=100,
                        help="Number of concurrent threads (default: 100)")
    parser.add_argument("-o", "--output", help="Save report to file (txt)")
    parser.add_argument("--timeout", type=float, default=0.5,
                        help="Socket timeout in seconds (default: 0.5)")
    return parser.parse_args()


def main():
    args = parse_args()
    scanner = PortScanner(timeout=args.timeout, max_threads=args.threads)

    print(f"\n🔍 Scanning {args.target} | Ports: {args.ports} | Threads: {args.threads}\n")
    results = scanner.scan(args.target, args.ports)

    reporter = Reporter(args.target, results)
    reporter.print_summary()

    if args.output:
        reporter.save(args.output)
        print(f"\n📄 Report saved to '{args.output}'")


if __name__ == "__main__":
    main()
