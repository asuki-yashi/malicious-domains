# Architecture

This project implements a simple but extensible threat-intel pipeline.

## Data Flow

```text
Public OSINT Feeds  -->  sources/ (raw)  -->  scripts/combine_feeds.py  -->  output/ (normalized)
