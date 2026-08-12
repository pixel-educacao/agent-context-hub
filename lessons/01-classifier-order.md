# 01 — Classifier order is a minefield

## What happened

The `who_kind` classifier is a deterministic cascade: check transactional domains → tool senders → tool domains → email-domain heuristic → name heuristic → unknown. The order is the whole design.

In production we hit the classic failure: `noreply@latam.com`. With the intuitive order (check "noreply" first), the airline became a **tool** — indistinguishable from GitHub notifications. The signal was lost: a flight confirmation is *transactional context*, not platform noise.

## The rule

```
transactional  >  tool senders  >  tool domains  >  person heuristics  >  unknown
```

Transactional domains (airlines, banks, insurance, government) must be checked **before** any generic tool/noreply rule. A `noreply@` prefix never overrides a transactional domain.

## Why it matters for you

The classifier decides how your agent *pays attention*. A misclassified airline confirmation and a marketing email look identical downstream. Order mistakes here are silent — nothing errors, the index just quietly lies.

**Test the boundary cases first:** `noreply@latam.com` (transactional), `support@acme.com` (tool), `maria@acme.com` (person), `Blueticket` (unknown). These four are the regression set — see `test_ledger.py`.
