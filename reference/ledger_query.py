#!/usr/bin/env python3
"""Query the Context Ledger — the first question the index answers.

Usage:
  python3 ledger_query.py                # last 7 days
  python3 ledger_query.py --since 30d    # bigger window
  python3 ledger_query.py --who acme     # filter by name/domain substring
  LEDGER_PATH=./my.jsonl python3 ledger_query.py

The ledger is NEVER loaded whole into agent context — this windowed view is
the only intended read path (see lessons/03-context-budget.md).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo(os.environ.get("CONTEXT_LEDGER_TZ", "America/Sao_Paulo"))
LEDGER = Path(os.environ.get("LEDGER_PATH", "context-ledger.jsonl"))


def parse_since(s: str) -> datetime:
    m = re.match(r"^(\d+)d$", s or "7d")
    if not m:
        raise SystemExit("use --since Nd (ex.: --since 7d)")
    return datetime.now(TZ) - timedelta(days=int(m.group(1)))


def load_rows(since: datetime):
    if not LEDGER.exists():
        return []
    rows = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        try:
            ts = datetime.fromisoformat(r["ts"])
        except Exception:
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=TZ)
        if ts >= since:
            rows.append(r)
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="7d")
    ap.add_argument("--who", default=None, help="substring filter on who/excerpt")
    ap.add_argument("--limit", type=int, default=15, help="max items shown")
    args = ap.parse_args()
    since = parse_since(args.since)

    rows = load_rows(since)
    if args.who:
        q = args.who.lower()
        rows = [r for r in rows if q in (r.get("who", "") + r.get("excerpt", "")).lower()]

    if not rows:
        print(f"Context — last {args.since}: no items in the ledger.")
        return 0

    by_source = Counter(r["source"] for r in rows)
    by_kind = Counter(r["who_kind"] for r in rows)
    who_count = Counter(r["who"] for r in rows)

    print(f"Context — last {args.since} ({len(rows)} items)")
    print()
    print("By source:  " + " · ".join(f"{k} {v}" for k, v in by_source.most_common()))
    print("By kind:    " + " · ".join(f"{k} {v}" for k, v in by_kind.most_common()))
    print()
    print("Top presences:")
    for who, n in who_count.most_common(6):
        print(f"  {who} ({n})")
    print()
    print("Items:")
    for r in rows[: args.limit]:
        print(f"  [{r['source']}/{r['who_kind']}] {r['who']} — {r['excerpt'][:60]}")
    if len(rows) > args.limit:
        print(f"  … +{len(rows) - args.limit} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
