# privacyTools

**Privacy-focused tools.**  
For now, this repo ships a single Windows 10/11 script: an **anti-Bitcoin-miner** detector/remover.  
Codename: **annaqualo**.

---

## What it is (today)
- **Anti-miner script (PowerShell):** scans for common persistence (Run/RunOnce, Tasks, Services), checks TEMP/AppData, and surfaces suspicious Chrome launches.  
- **Scope:** detect and remove typical Bitcoin mining footholds; produce a plain log for review.

> Transparent by design: no telemetry, no external modules, readable code.

---

## Requirements
- Windows 10 or Windows 11  
- PowerShell 5.0+

---
