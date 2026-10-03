"""Reads inventory.json, checks each device by TCP connect, prints UP/DOWN, saves output.json."""
import json
import socket
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent
TIMEOUT = 2  # seconds


def check_device(ip, port):
    """Return 'UP' if a TCP connection succeeds, else 'DOWN'."""
    try:
        with socket.create_connection((ip, port), timeout=TIMEOUT):
            return "UP"
    except OSError:
        return "DOWN"


def main():
    try:
        devices = json.loads((BASE / "inventory.json").read_text())
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"Cannot read inventory.json: {exc}")
        sys.exit(1)

    results = []
    print(f"{'Hostname':<12} {'IP':<14} {'Port':<5} Status")
    print("-" * 40)
    for d in devices:
        try:
            status = check_device(d["ip"], int(d.get("port", 22)))
        except (KeyError, ValueError) as exc:
            print(f"Skipping invalid entry {d}: {exc}")
            continue
        print(f"{d['hostname']:<12} {d['ip']:<14} {d.get('port', 22):<5} {status}")
        results.append({**d, "status": status,
                        "checked_at": datetime.now().isoformat(timespec="seconds")})

    (BASE / "output.json").write_text(json.dumps(results, indent=2))
    up = sum(r["status"] == "UP" for r in results)
    print(f"\n{up} of {len(results)} devices UP. Results saved to output.json")


if __name__ == "__main__":
    main()
