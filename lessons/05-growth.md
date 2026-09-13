# 05 — Growth is bounded by design

## What happened

People's first worry about an append-only ledger: "won't this grow forever?" It does grow forever — that's fine, because every design choice bounds the *cost* of growth, not the size.

## The four bounds

1. **Excerpt cap (~200 chars).** The ledger stores a trace, not the content. The excerpt is bounded; total row size also depends on other fields, which the toy does not cap. Full text lives at the source, reachable by `ref` through the integrator.
2. **Dedupe by ref.** Re-pulling a source never grows the ledger. Growth is proportional to *new signals*, not to how often you pull.
3. **Rotation, not pruning.** When the file gets large (ours: ~64KB at 201 rows; the cliff is many MB away), rotate quarterly archives and keep ~90 days hot. Append-only means rotation is a file move, never a rewrite.
4. **Query windows.** The window (`--since`) bounds the selected result, not disk I/O: the reference CLI reads the entire JSONL file before filtering. `--limit` bounds displayed items. Neither option implements retention or indexed access.

## The one known cliff

`append_entry` re-reads all refs on every write: O(n) per append. The original note's approximate threshold of 100k rows was not a published benchmark and must not be treated as an SLA. Measure complete row sizes, storage and workload before deciding when to use a sidecar set or SQLite table. Avoid speculative optimization, but do not assume an unmeasured performance guarantee.

## Rule of thumb

Estimate storage from complete serialized rows, not the excerpt alone. Include JSON metadata, UTF-8 byte sizes and uncapped fields. Measure query and append latency with the intended workload; the reference repo includes neither a benchmark-derived cliff nor automatic rotation.
