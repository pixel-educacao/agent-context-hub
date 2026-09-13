# 03 — Never load the ledger whole

## What happened

The natural instinct is: "the ledger is small, just load it into the agent's context every session." Don't.

The ledger is an **index**, and indexes grow without bound — that's the point. Loading it whole couples your context budget to your intake volume. A founder capturing from 5 sources produces hundreds of rows per week; within months the "small file" eats a meaningful slice of every conversation's context window, most of it irrelevant to the current task.

## The pattern

```
agent needs context → windowed query → small relevant slice
                    NEVER → cat ledger.jsonl → whole file into context
```

- The only read path is a **windowed query**: `--since 7d`, `--who <name>`, `--since 30d`.
- The query returns a *digest* (counts by source, top presences, first N items) — not raw rows.
- When a row matters, follow its `ref` to the original source for full content. **Reference CLI limitation:** the displayed digest does not include each item's `ref` or timestamp. The integrator must retrieve those fields from the matching JSONL row without dumping the whole file into the agent's context. The toy does not include an external-source resolver.

## The number that convinced us

Production ledger: 201 rows, 64KB, five sources, three weeks. The windowed query for a typical session returned 59 relevant rows and the agent never saw more than 15 item lines. Context cost: a digest. Without the window: 64KB on *every* turn, growing forever.

## Rule

If you find yourself writing code that reads the whole ledger outside of the query tool, stop. That's a new index field or a summary layer asking to be born — not a context load.
