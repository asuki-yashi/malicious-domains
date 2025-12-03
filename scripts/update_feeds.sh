#!/usr/bin/env bash
set -euo pipefail

# Simple feed updater for malicious-domains project
# This script downloads/refreshes all configured feeds into the sources/ directory.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="$ROOT_DIR/sources"

mkdir -p "$SRC_DIR"

# TODO: Replace placeholder URLs with actual public feed URLs where applicable.
declare -A FEEDS=(
  ["alienvault-banking-phishtank"]="https://example.com/alienvault-banking-phishtank.txt"
  ["alienvault-cert-pl"]="https://example.com/alienvault-cert-pl.txt"
  ["alienvault-cobalt-strike"]="https://example.com/alienvault-cobalt-strike.txt"
  ["alienvault-dropbox-phishtank"]="https://example.com/alienvault-dropbox-phishtank.txt"
  ["alienvault-googledocs-phishtank"]="https://example.com/alienvault-googledocs-phishtank.txt"
  ["alienvault-microsoft-phishtank"]="https://example.com/alienvault-microsoft-phishtank.txt"
  ["alienvault-paypal-phishtank"]="https://example.com/alienvault-paypal-phishtank.txt"
  ["alienvault-phishing-scam"]="https://example.com/alienvault-phishing-scam.txt"
  ["digitalside.it.txt"]="https://example.com/digitalside.it.txt"
  ["drb-ba.txt"]="https://example.com/drb-ba.txt"
  ["malwarebytes.com.txt"]="https://example.com/malwarebytes.com.txt"
  ["openphish.com"]="https://example.com/openphish.csv"
  ["phishing_army"]="https://example.com/phishing_army_blocklist.txt"
  ["phishtank.com-online-valid"]="https://example.com/phishtank-online-valid.csv"
  ["phishunt.io.txt"]="https://example.com/phishunt.io.txt"
  ["red.flag.domains.txt"]="https://example.com/red.flag.domains.txt"
  ["urlhaus.abuse.ch-csv"]="https://example.com/urlhaus.csv"
  ["urlhaus.abuse.ch-hostfile"]="https://example.com/urlhaus.hosts"
  ["ut1-fr"]="https://example.com/ut1-fr.txt"
)

echo "[*] Updating feeds into: $SRC_DIR"
for NAME in "${!FEEDS[@]}"; do
  URL="${FEEDS[$NAME]}"
  OUT_FILE="$SRC_DIR/$NAME"
  echo "[*] Downloading $NAME from $URL"
  if curl -fsSL "$URL" -o "$OUT_FILE.tmp"; then
    mv "$OUT_FILE.tmp" "$OUT_FILE"
  else
    echo "[!] Failed to download $NAME from $URL"
    rm -f "$OUT_FILE.tmp" || true
  fi
done

echo "[+] Feed update complete."

