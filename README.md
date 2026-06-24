# Ghost Protocol: Digital Relocation & OPSEC Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Platform: macOS](https://img.shields.io/badge/Platform-macOS-blue.svg?style=flat-square)]()
[![Backend: Python 3](https://img.shields.io/badge/Language-Python%203-blue.svg?style=flat-square)]()
[![Security: Tor](https://img.shields.io/badge/Network-Tor%20obfs4-purple.svg?style=flat-square)]()

## Overview
Ghost Protocol is an advanced defensive automation framework designed for comprehensive digital relocation, identity spoofing, and system hardening on macOS (Darwin). It surgically modifies deep network stacks to enforce encrypted routing.

## Problem Statement
Standard VPNs and proxy configurations are insufficient for true anonymity due to local DNS leaks, heuristic timezone tracking, and hardware telemetry (Bluetooth beacons). Security researchers require a "one-click" kill-switch that synchronizes the host operating system's internal state with its external proxy footprint.

## Key Features
- **Volatile RAM Containerization:** Allocates a 1GB RAM Disk for browser isolation. Cache and cookies physically evaporate upon reboot.
- **Hardware Decapitation:** Unloads `coreaudiod` and `AppleCameraAssistant` to sever zero-day acoustic/visual attack vectors.
- **Kernel-Level Chronology Spoofing:** Syncs the deep system clock (`locationd`, NTP) with the exact timezone of the current Tor exit node.
- **Oblivious DNS-over-HTTPS (ODoH):** Hijacks native resolvers to tunnel DNS queries through encrypted endpoints.

## Architecture

```mermaid
graph TD
    User[macOS User Environment] -->|SOCKS5 Proxy| TorDaemon[Local Tor Daemon :9050]
    TorDaemon -->|obfs4 Obfuscation| EntryNode[Tor Entry Node]
    EntryNode -->|Encrypted Circuit| RelayNode[Tor Relay]
    RelayNode -->|Exit Override| ExitNode[Target Country Exit Node]
    ExitNode -->|Clearnet| TargetWebsite[Destination Server]
    
    sublayer[Ghost Protocol Interventions] -->|Timezone Sync| User
    sublayer -->|Kill-switch Monitor| TorDaemon
    sublayer -->|Hardware Disablement| MacDaemons[Camera/Mic/Bluetooth]
```

## Technology Stack
- **Core Engine:** Python 3.12
- **Network Layer:** Tor, obfs4proxy, SOCKS5
- **System Interface:** macOS `launchctl`, `scutil`, `networksetup`
- **UI Terminal:** `curses`, ANSI terminal formatting

## Project Structure
```text
GhostProtocol/
├── GhostProtocol.py          # Main monolithic OPSEC execution engine
├── test_ghost_protocol.py    # Subprocess mocking and logic tests
└── README.md                 # System architecture and documentation
```

## Installation
Administrator privileges are strictly required.
```bash
brew install tor
git clone https://github.com/krsna016/GhostProtocol.git
cd GhostProtocol
```

## Usage
Execute the script using a privileged Python environment:
```bash
sudo python3 GhostProtocol.py
```

## Examples
*Terminal Output Example during routing override:*
```text
[+] Initiating Tor Bootstrap Sequence...
[+] Hijacking DNS Resolvers -> 1.1.1.1
[+] Enforcing Exit Node Strictness: CH, RU, IS
[+] Hardware Decapitation: Audio/Visual Daemons Unloaded.
```

## Screenshots
> [!NOTE]
> *Aggressive OPSEC UI terminal screenshots are pending capture for the V4 release.*

## Visual Demonstrations
> [!NOTE]
> *Video demonstrations of the Volatile RAM containerization are currently being recorded.*

## Testing
Core shell execution and daemon termination logic is validated via `unittest` mocking to prevent destructive testing on host systems.
```bash
python3 -m unittest test_ghost_protocol.py
```

## Performance Notes
- **obfs4 Obfuscation:** Pluggable transports induce a 15-20% latency penalty but successfully evade Deep Packet Inspection (DPI) heuristics.
- **RAM Disks:** The 1GB Volatile Container requires at least 8GB of total system memory to prevent macOS swapping.

## Future Improvements
- **Modularity:** The monolithic `GhostProtocol.py` must be decoupled into independent `network`, `hardware`, and `ui` packages.
- **MAC Randomization:** Implement a bypass for Apple Silicon's hardcoded MAC address restrictions using custom kernel extensions.

## Contributing
Pull requests must focus purely on defensive OPSEC configurations. Offensive modules will be rejected.

## Legal & White-Hat Usage Disclaimer
This framework is engineered exclusively for **theoretical exploration, academic analysis, and ethical red-team defense operations**. It actively modifies deep macOS network stacks, routing tables, and kernel daemons. 

**Do not deploy this software on production machines or networks where you do not have explicit, written authorization.** The authors and contributors are absolutely not responsible for any misuse, system instability, or illegal activities conducted utilizing this repository. Code is provided "AS-IS" for cybersecurity education.

## License
Licensed under the MIT License.
