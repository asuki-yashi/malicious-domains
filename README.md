# Malicious Domains – Open Threat Intelligence Feed Aggregator

This repository aggregates multiple **public threat intelligence (TI) data sources** into a single, normalized, and de-duplicated list of malicious, phishing, C2, and suspicious domains.

The goal is to provide a **clean, ready-to-consume IOC dataset** for:
- SOC & DFIR teams
- Blue-team threat hunting
- SIEM lookup enrichment
- DNS/Firewall blocking
- OSINT/CTI research

---

#  Key Features

✔ Aggregates 19+ raw feeds  
✔ Extracts domains using strict regex  
✔ Automatically deduplicates  
✔ Deterministic sorted output (stable Git diffs)  
✔ CI/CD ready feed pipeline  
✔ Designed for SOC production environments  

---

#  Repository Layout

```

malicious-domains/
├── sources/           # Raw upstream threat intel feeds
├── scripts/           # TI ingestion + normalization pipeline
│   ├── update_feeds.sh
│   └── combine_feeds.py
├── output/            # Final unified domain lists
│   ├── domains.txt
│   └── domains.csv
├── docs/              # Engineering documentation
│   ├── ARCHITECTURE.md
│   ├── DATA_MODEL.md
│   └── FEED_SOURCES.md
└── CONTRIBUTING.md

````

---

#  Architecture Summary

The pipeline follows a clean separation of layers:

```text
[Raw OSINT Feeds]  -->  sources/
                        (untouched)

sources/ --> combine_feeds.py
             (parse + extract + dedupe)

combine_feeds.py --> output/
                     (normalized artifacts)
````

Principles:

* **Lossless ingestion** (retain original data in `sources/`)
* **Normalization only in scripts**
* **Idempotent runs**
* **Deterministic ordering**

More visuals: see [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

---

#  Running the Pipeline

##  Update feeds (optional)

> You can wire this script to cron or a GitHub Action.

```bash
./scripts/update_feeds.sh
```

This refreshes raw `.txt` feed files in `sources/`.

> NOTE: Replace placeholder URLs in the script with real feed URLs.

---

##  Combine & Normalize

```bash
python3 scripts/combine_feeds.py
```

Outputs generated under `output/`:

| File          | Purpose                                                      |
| ------------- | ------------------------------------------------------------ |
| `domains.txt` | One domain per line list (ready for DNS/firewall)            |
| `domains.csv` | CSV format with header (SIEM lookup tables, SOAR enrichment) |

---

#  Indicators Data Model

* Indicator type: **Domain**
* Regex-based strict extraction
* Canonical form: lower-cased domain only
* No URLs, IPs, paths, or protocols

Future metadata planned:

* source feed
* threat type (phishing/malware/c2)
* first_seen / last_seen timestamps
* confidence score

More details: [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md)

---

#  Feed Sources

All OSINT-provider files are located in `sources/`.

Mapping details: [`docs/FEED_SOURCES.md`](docs/FEED_SOURCES.md)

---

#  Practical Integration Examples

##  SOC / SIEM Threat Enrichment

Upload `output/domains.csv` as:

* A lookup table
* Dynamic blacklist
* Enrichment dataset

Use case:

* When DNS/Proxy/Firewall logs contain a domain:

  * check membership in this list
  * tag as suspicious
  * map to threat intelligence source

---

##  DNS Blocking (Pi-hole, Bind, Unbound)

Convert domains to hosts file format:

```
0.0.0.0 bad-domain.example
```

Example:

```bash
sed 's/^/0.0.0.0 /' output/domains.txt > output/hosts.txt
```

Use `hosts.txt` as blocklist.

---

##  Firewall (Fortigate / Palo Alto)

Convert to bulk blacklist import format.

Example URL pattern:

```
*.malicious-domain.com
```

> Future plan: auto-generate firewall import format.

---

##  SOAR Automation

Feed `domains.csv` into:

* Cortex XSOAR playbooks
* Shuffle automations
* ANY SOC custom enrichment microservice

---

#  Research & OSINT Use Cases

✔ Malicious infra trend analysis
✔ Domain age profiling
✔ Malware campaign correlation
✔ TI scoring models
✔ WhoIs intel pivoting
✔ APT/C2 infra clustering

---

# 🛠 Roadmap

* Add automated feed ingestion via GitHub Actions
* Export artifacts:

  * STIX
  * MISP JSON
  * hosts file
* Add metadata annotations:

  * threat_type
  * first_seen
  * confidence
* Build lookup API for realtime domain reputation:

  ```
  GET /lookup?domain=xyz.com
  ```

---

#  Contributing

Contributions welcome!

Please check [`CONTRIBUTING.md`](CONTRIBUTING.md)

---

#  Disclaimer

All data are collected for:

* research
* blue-team defensive security
* SOC/Threat Intel usage only

❗ Do NOT use this dataset for any offensive or unlawful purpose.
❗ Maintainer holds no liability for misuse.

