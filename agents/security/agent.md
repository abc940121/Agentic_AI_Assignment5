# Security Agent
## Responsibilities
- Protect the knowledge graph from malicious queries (injection, deletion, etc.).
- Filter out queries that violate school safety or academic integrity policies.

## Implementation
- Implements a strict **Keyword Blacklist** (e.g., DELETE, DROP, BYPASS).
- Cross-references with NLU classification for redundancy.
- Returns a `REJECT` decision with a clear reason if a threat is detected.
