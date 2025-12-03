# Data Model

The project currently focuses on **domains** as the primary indicator type.

## Canonical Domain Representation

- Lowercase string
- No protocol prefix (`http://`, `https://`)
- No path, query string, or fragment
- Punycode or Unicode: stored as ingested (future: normalization)

Examples:

- ✅ `login.example.com`
- ❌ `https://login.example.com/index.php?user=...`
- ❌ `192.168.1.10`

## Future Fields (Planned)

In extended formats (CSV/JSON), we may later add:

- `domain` (string, required)
- `source_feed` (string)
- `first_seen` / `last_seen` (timestamps)
- `threat_type` (`phishing`, `malware`, `c2`, `generic`, ...)
- `confidence` (0–100)
- `tags` (e.g. `["banking", "ransomware", "office365"]`)
