# Local Network Port Scanner

## Description
A fast, multi-threaded CLI port scanner that checks which TCP ports are open on a target host. Identifies common services and attempts banner grabbing.

## Features
- Multi-threaded scanning (configurable thread count)
- Port range or comma-separated port list
- Service name identification for well-known ports
- Banner grabbing for open ports
- Save results to a text report

## Tech Stack
- Python 3.10+
- `socket`, `concurrent.futures`, `argparse`

## Installation
```bash
pip install -r requirements.txt
```

## How to Run
```bash
# Scan common ports on localhost
python main.py 127.0.0.1

# Scan specific ports
python main.py 192.168.1.1 -p 22,80,443,8080

# Scan a range with more threads
python main.py scanme.nmap.org -p 1-500 -t 200

# Save report
python main.py 127.0.0.1 -o report.txt
```

## Example Output
```
[OPEN] Port    22/tcp  SSH
[OPEN] Port    80/tcp  HTTP

PORT       SERVICE         BANNER
22         SSH             SSH-2.0-OpenSSH_8.9
80         HTTP
Total open: 2
```
