#!/usr/bin/env python3
"""
Combine multiple raw threat-intel feeds into a single, normalized, de-duplicated domain list.

Design goals:
- Idempotent: running multiple times produces same output for same input
- Deterministic ordering for version control diffs
- Efficient for large feeds (set-based de-duplication)
"""

from __future__ import annotations
import re
import csv
from pathlib import Path
from typing import Iterable, Set

ROOT_DIR = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT_DIR / "sources"
OUTPUT_DIR = ROOT_DIR / "output"

DOMAIN_REGEX = re.compile(
    r"\b([a-zA-Z0-9][a-zA-Z0-9\-]{0,62}\.)+[a-zA-Z]{2,}\b"
)

def extract_domains_from_line(line: str) -> Iterable[str]:
    """
    Extract candidate domains from a single line using a regex.
    """
    line = line.strip()
    if not line or line.startswith("#"):
        return []

    # Hosts file style: "0.0.0.0 bad.domain.com"
    parts = line.split()
    if len(parts) >= 2 and parts[0].replace(".", "").isdigit():
        line = parts[1]

    matches = DOMAIN_REGEX.findall(line)
    return [m.lower() for m in matches]


def collect_domains() -> Set[str]:
    """
    Walk through the sources/ directory and collect all unique domains.
    """
    domains: Set[str] = set()

    if not SOURCES_DIR.exists():
        raise SystemExit(f"[!] Sources directory not found: {SOURCES_DIR}")

    for path in SOURCES_DIR.rglob("*"):
        if not path.is_file():
            continue

        try:
            with path.open("r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    for domain in extract_domains_from_line(line):
                        domains.add(domain)
        except Exception as exc:  # noqa: BLE001
            print(f"[!] Failed to parse {path}: {exc}")

    return domains


def write_outputs(domains: Set[str]) -> None:
    """
    Write normalized outputs:
    - output/domains.txt  (one domain per line)
    - output/domains.csv  (domain column)
    """
    OUTPUT_DIR.mkdir(exist_ok=True)

    sorted_domains = sorted(domains)

    txt_path = OUTPUT_DIR / "domains.txt"
    csv_path = OUTPUT_DIR / "domains.csv"

    with txt_path.open("w", encoding="utf-8") as f:
        for d in sorted_domains:
            f.write(d + "\n")

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["domain"])
        for d in sorted_domains:
            writer.writerow([d])

    print(f"[+] Wrote {len(sorted_domains)} unique domains")
    print(f"[+] TXT:  {txt_path}")
    print(f"[+] CSV:  {csv_path}")


def main() -> None:
    domains = collect_domains()
    write_outputs(domains)


if __name__ == "__main__":
    main()
