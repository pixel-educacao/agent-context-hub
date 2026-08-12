# 02 — Hook producers at write time, backfill later

## What happened

We had five producers writing raw signals (meeting notes, chat threads, email scans). Three of them appended to the ledger the day they were built. Two — meeting transcripts from a transcription tool and a meeting assistant with 34 files already on disk — had the hook added later, and landed with **zero** ledger entries despite weeks of captured data.

The fix was trivial because of dedupe: backfill by scanning the existing raw files and calling `append_entry` with the same ref scheme. 34 files → 34 entries, zero duplicates, idempotent.

## The rules

1. **Append at write time.** The moment a producer writes the raw file, it appends the ledger row in the same code path. Not "later", not "in the digest step" — the write is the hook point.
2. **Refs must be deterministic.** `source:stable-id` where the id comes from the source (message id, note id, email id, event uid) — never a local timestamp or counter. Deterministic refs are what make backfills, reruns, and restarts safe.
3. **Backfill is always possible** as long as the raw data is on disk and refs are deterministic. You never lose the ability to index history.

## Anti-pattern we avoided

A separate "indexer" process that re-reads all raw files on a schedule. It works, but it reintroduces the exact drift problem the hook eliminates: any gap between "raw exists" and "indexer ran" is a window where your agent doesn't know its own context.
