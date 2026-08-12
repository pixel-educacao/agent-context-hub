#!/usr/bin/env python3
"""Smoke tests for the Context Ledger reference implementation.

Run: python3 test_ledger.py
No dependencies — exits non-zero on first failure.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import context_ledger as cl


def test_classifier_order():
    # transactional must win over tool, even for noreply senders
    assert cl.classify_who("LATAM", "noreply@latam.com") == "transactional", \
        "transactional senders must not be classified as tools"
    assert cl.classify_who("Booking.com", "confirm@booking.com") == "transactional"
    # tools
    assert cl.classify_who("GitHub", "noreply@github.com") == "tool"
    assert cl.classify_who("Fathom", "noreply@fathom.video") == "tool"
    assert cl.classify_who("Support", "support@acme.com") == "tool"
    # persons
    assert cl.classify_who("Maria Santangelo", "maria@rj.senac.br") == "person"
    assert cl.classify_who("Ana Souza", "") == "person"
    # unknown
    assert cl.classify_who("Blueticket", "") == "unknown"
    assert cl.classify_who("x", "") == "unknown"
    print("ok: classifier order")


def test_excerpt_truncation():
    long_text = "word " * 200
    cleaned = cl.clean_excerpt(long_text)
    assert len(cleaned) <= cl.EXCERPT_MAX + 1  # +1 for ellipsis
    assert cleaned.endswith("…")
    assert cl.clean_excerpt("  a\n\n  b  ") == "a b"
    print("ok: excerpt truncation")


def test_append_and_dedupe():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test-ledger.jsonl"

        # first append succeeds
        assert cl.append_entry(
            source="meetings", who="Meetings: Sync (Ana)",
            excerpt="Ana owns the deck", ref="meetings:001",
            who_kind="tool", path=path,
        ) is True

        # same ref is deduped
        assert cl.append_entry(
            source="meetings", who="Meetings: Sync (Ana)",
            excerpt="Ana owns the deck", ref="meetings:001",
            who_kind="tool", path=path,
        ) is False

        # different ref appends
        assert cl.append_entry(
            source="meetings", who="Meetings: Call (Carla)",
            excerpt="Carla wants a quote", ref="meetings:002",
            who_kind="tool", path=path,
        ) is True

        rows = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
        assert len(rows) == 2, f"expected 2 rows, got {len(rows)}"

        # schema is exactly the 6 fixed fields
        expected = {"ts", "source", "who", "who_kind", "excerpt", "ref"}
        for r in rows:
            assert set(r.keys()) == expected, f"schema drift: {set(r.keys())}"
    print("ok: append + dedupe + schema")


def test_query_window():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test-ledger.jsonl"
        cl.append_entry(source="a", who="X", excerpt="e", ref="a:1", path=path)
        # point the env at our temp file and query
        os.environ["LEDGER_PATH"] = str(path)
        # reload module-level constant
        import importlib
        import ledger_query
        importlib.reload(ledger_query)
        rows = ledger_query.load_rows(ledger_query.parse_since("7d"))
        assert len(rows) == 1, f"expected 1 row in window, got {len(rows)}"
    print("ok: query window")


def main() -> int:
    test_classifier_order()
    test_excerpt_truncation()
    test_append_and_dedupe()
    test_query_window()
    print("\nAll smoke tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
