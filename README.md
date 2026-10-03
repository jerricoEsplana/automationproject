# Mini Network Automation Project

## Purpose
Checks the reachability of Cisco network devices listed in `inventory.json`
and reports each one as **UP** or **DOWN**.

## Files
| File | Description |
|------|-------------|
| `inventory.json` | Device list (hostname, ip, device_type, location, port) |
| `network_check.py` | Reads the inventory, checks each device, prints and saves results |
| `output.json` | Generated results, including a timestamp per device |

## How it works
For each device the script tries a TCP connection to `ip:port` (2 s timeout).
Success = `UP`, failure/timeout = `DOWN`. For real devices use port 22 (SSH) or 443.
The sample inventory uses `127.0.0.1` (port 8022 open only if you start `python -m http.server 8022`; port 9 closed) and a
non-routable address (`192.0.2.10`) so the check is a safe simulation.

## Usage
```
python network_check.py
```
Requires Python 3 only (standard library).

## Error handling
Missing/invalid `inventory.json` exits with a message; malformed entries are skipped;
connection errors and timeouts are reported as DOWN.
