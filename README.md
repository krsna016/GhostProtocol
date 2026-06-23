# Ghost Protocol - V2 (Advanced OPSEC)

▶ An advanced, high-level defensive automation framework designed for comprehensive digital relocation and identity spoofing on macOS (Darwin).

## V2 Advanced OPSEC Upgrades
- **Wi-Fi Kill-Switch**: A background thread actively monitors the Tor daemon. If Tor crashes, the framework physically drops the Wi-Fi interface (`en0`), preventing IP leaks.
- **Dynamic Hostname Scrambling**: Uses `scutil` to mathematically randomize the machine's broadcast hostname to evade local network fingerprinting.
- **Oblivious DNS-over-HTTPS (ODoH)**: Hijacks network resolvers to inject Cloudflare encrypted DNS (1.1.1.1), blinding local ISPs from domain queries.
- **Forensic Log Obliteration**: Flushes the system DNS cache (`dscacheutil`) and triggers a deep wipe of active connection metadata upon reverting.
- **Quarantine Containerization**: Spawns highly isolated Chromium processes that are strictly funneled through Tor, bypassing master system routing.

## Architecture & Mechanics

Ghost Protocol executes mathematically verifiable digital plastic surgery across multiple system layers to evade endpoint telemetry, browser fingerprinting, and geolocation trackers.

It operates by manipulating three core attack surfaces:
1.  **Hardware Layer Masking (Air-Gap Simulation):** Scrambles system hostnames dynamically to blind 802.11 network probes. (Note: MAC spoofing is physically locked out on Apple Silicon M-series hardware).
2.  **Kernel-Level Chronology Spoofing:** To defeat JavaScript-based Timezone API validation and heuristic telemetry, Ghost Protocol physically intercepts macOS's `locationd` and Network Time Protocol (NTP) daemons, coercing the deep system clock into matching the target exit node's locale.
3.  **Encrypted Circuit Routing (Tor Engine):** The application programmatically rewrites the Tor `torrc` configuration to mandate strict exit node compliance. It then alters the host machine's SOCKS5 proxy state to forcefully tunnel all outbound TCP traffic through the local 9050 port.

## Deployment Requirements
- macOS (Darwin) architecture
- Homebrew environment
- Tor binary (`brew install tor`)
- Administrator privileges (for raw system manipulation)

## Usage Disclaimer
This framework is engineered exclusively for theoretical exploration, academic analysis, and ethical defense operations. It requires root-level authorization to modify core network stacks.
