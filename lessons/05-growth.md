# 05 — Growth is bounded by design

## What happened

People's first worry about an append-only ledger: "won't this grow forever?" It does grow forever — that's fine, because every design choice bounds the *cost* of growth, not the size.

## The four bounds

1. **Excerpt cap (~200 chars).** The ledger stores a trace, not the content. Row size is bounded regardless of source. Full text lives at the source, reachable by `ref`.
2. **Dedupe by ref.** Re-pulling a source never grows the ledger. Growth is proportional to *new signals*, not to how often you pull.
3. **Rotation, not pruning.** When the file gets large (ours: ~64KB at 201 rows; the cliff is many MB away), rotate quarterly archives and keep ~90 days hot. Append-only means rotation is a file move, never a rewrite.
4. **Query windows.** Read cost is bounded by the window (`--since`), not by total size.

## The one known cliff

`append_entry` re-reads all refs on every write — O(n) per append. Perfectly fine to ~100k rows (sub-second on local disk). Beyond that, keep refs in a sidecar set or a small SQLite table. We documented the cliff instead of pre-building for it: **no speculative optimization until a real volume demands it** — same rule as ledger fields.

## Rule of thumb

At 200 chars/row, 100k rows ≈ 20MB. If you capture 100 signals/day, that's ~3 years before you hit the cliff. Build the rotation script when you need it, not before.
