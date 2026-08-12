# 06 — Query-first, not log-first

## What happened

The ledger was designed from the query backwards. Before writing any producer, we fixed the first question the index must answer:

> "What arrived, from whom, when — in the last N days?"

Everything else followed: the six fields exist because that query needs them; no field exists that the query doesn't. The query CLI (`ledger_query.py`) shipped with the first producer, not after the fifth.

## Why log-first fails

The default engineering move is to log first ("capture everything, we'll query later") and build the read path when someone asks. In production this produces:

- **Fields nobody queries** — every speculative field is maintenance debt with no consumer.
- **No adoption** — a write-only log proves nothing; nobody trusts an index they've never seen answer.
- **Schema drift** — without a fixed contract, each producer invents its own shape, and dedupe/merge becomes a project.

## The discipline

1. **Fix the query before the first producer.** If you can't state the question, you're not ready to capture.
2. **A new field requires a real query that needs it.** "Might be useful" is not a query.
3. **Ship the query tool with producer #1.** The index earns trust by answering on day one.
4. **Corrections are new rows.** Append-only means the log is also an audit trail — you can see context arriving, not just context existing.

## The payoff

Three weeks in, the ledger answered real questions without touching the sources: "did the conference organizer reply?", "who's been most present this week?", "what came from meetings vs email?". Each answer was one windowed query. That's the product.
