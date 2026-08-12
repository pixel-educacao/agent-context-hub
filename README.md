# Agent Context Hub

> **The pattern:** every signal that reaches your AI agent — meetings, chat, email, calendar — gets appended to one unified, append-only **Context Ledger**. The ledger is an index, not storage: it answers *"what came in, from whom, when"* so your agent always knows its own recent context without loading raw data.

Built from lessons learned running this exact system in production for a founder's second brain (WhatsApp, Gmail, Granola, Fathom, calendar invites — five producers, one ledger).

```
source A (meetings API) ─┐
source B (chat export)  ─┤
source C (email scan)   ─┼──► ContextItem (6 fields) ──► context-ledger.jsonl ──► windowed query
source D (calendar)     ─┘          append-only, dedupe by ref                ("what arrived this week?")
```

## Why a ledger and not just a database?

1. **Capture must be cheap and dumb.** Producers append one line per signal, no interpretation. If capture needs an LLM or a judgment call, it will silently rot the index.
2. **Raw ≠ memory.** The ledger is a *map* of what arrived. The actual content stays at the source (or in a raw queue your semantic index must never touch). Analysis happens at read time, on demand.
3. **Dedupe makes every producer re-runnable.** Pull-based capture with stable refs means reruns, backfills, and restarts are all safe by construction.

## Repo contents

| Path | What |
|---|---|
| [`reference/context_ledger.py`](reference/context_ledger.py) | The ledger: schema, deterministic classifier, append with dedupe |
| [`reference/ledger_query.py`](reference/ledger_query.py) | Windowed query CLI (`--since 7d --who <name>`) |
| [`reference/example_producer.py`](reference/example_producer.py) | Minimal producer showing the hook pattern |
| [`reference/test_ledger.py`](reference/test_ledger.py) | Smoke tests (schema, dedupe, classifier order) |
| [`lessons/`](lessons/) | The production lessons, organized by theme |

## 5-minute start

```bash
cd reference
python3 context_ledger.py            # self-smoke: classifier checks
python3 example_producer.py          # appends 3 synthetic signals
LEDGER_PATH=./demo-ledger.jsonl python3 ledger_query.py --since 7d
python3 test_ledger.py               # all smoke tests
```

That's the whole loop: **capture → ledger → windowed query**. Add real producers by copying `example_producer.py` and pointing it at your source.

## The contract (what never changes)

Six fixed fields per entry:

| Field | Meaning |
|---|---|
| `ts` | ISO timestamp, local timezone |
| `source` | producer id (`gmail`, `whatsapp`, `granola`, `fathom`, `calendar`, …) |
| `who` | sender exactly as it arrived |
| `who_kind` | `person` \| `tool` \| `transactional` \| `unknown` (deterministic) |
| `excerpt` | raw text, ~200 chars, never interpreted |
| `ref` | stable id for dedupe + tracing back to the original |

Design locks (from production):

- **Append-only.** Corrections are new rows, never edits.
- **Dedupe by `ref`.** Re-pulling a source must never duplicate.
- **No interpretation at capture.** The excerpt is raw text; classification is a deterministic denylist + heuristic, never an LLM call.
- **New fields only when a real query demands them.** Every speculative field you add is a lie you'll maintain forever.

## Lessons learned

The short version — full write-ups with context in [`lessons/`](lessons/):

1. **[Classifier order is a minefield](lessons/01-classifier-order.md)** — transactional senders (`noreply@latam.com`) must be checked *before* generic tool rules, or airlines become "tools".
2. [Hook producers at write time, backfill later](lessons/02-producer-hooks.md) — append when you write the raw file; dedupe makes history backfillable.
3. [Never load the ledger whole](lessons/03-context-budget.md) — windowed queries only; the ledger never enters agent context in full.
4. [Keep raw queues out of your semantic index](lessons/04-index-hygiene.md) — searchable memory stores the curated; the ledger answers the intake question.
5. [Growth is bounded by design](lessons/05-growth.md) — 200-char excerpts + dedupe + rotation; the O(n) ref check has a known cliff (~100k rows).
6. [Query-first, not log-first](lessons/06-query-first.md) — a ledger you can't query on day one is just a log file.

## Requirements

Python 3.9+ standard library only. No dependencies, no server, no database.

## License

MIT — see [LICENSE](LICENSE).
