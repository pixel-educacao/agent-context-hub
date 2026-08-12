# 04 — Keep raw queues out of your semantic index

## What happened

We run two retrieval systems and learned to keep them strictly separated:

1. **The Context Ledger** — append-only intake index. Answers *"what came in, from whom, when"*.
2. **The semantic index (embeddings/FTS)** — searchable memory of the brain. Answers *"what do we know about X"*.

The early temptation was to index everything, including the raw capture queues (chat exports, meeting-note queues, transcript dumps). That's a trap, for two reasons:

- **Quality:** re-pollable raw queues contain thousands of near-duplicate fragments ("ok", "blm", "(mídia sem texto)") that compete with real knowledge for retrieval ranking. Search quality degrades silently.
- **Privacy:** raw queues are the least-curated data you have. Indexing them means they flow into whatever downstream processing the index feeds (in our case: an embedding API). Raw-in-index became a reportable incident in our operating rules.

## The rule

```
raw capture queues  →  ledger (intake map)  →  curation  →  semantic index
                          ↑                        ↑
                    never indexed            the only gate to
                    semantically             searchable memory
```

- The semantic index's allowlist **excludes raw/queue directories by policy**, not by accident.
- The ledger is the *map* of what exists in the raw queues, so you never need to index them to know what's there.
- Only curated/destilled content crosses into searchable memory.

## How to check yours

Grep your index build config for the queue paths. If a raw directory is reachable by the indexer's include globs, it's a bug — even if it "hasn't mattered yet".
