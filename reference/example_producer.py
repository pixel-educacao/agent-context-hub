#!/usr/bin/env python3
"""Minimal producer — the hook pattern every source follows.

Copy this file, point it at your source (API pull, export scan, inbox read),
and call `append_entry` once per signal. The contract is the only thing that
matters: source id, who, raw excerpt, stable ref.

Stable refs are what make pull-based capture re-runnable: if the ref is
deterministic (message id, note id, email id, event uid), reruns and
backfills never duplicate. See lessons/02-producer-hooks.md.
"""
from __future__ import annotations

import context_ledger as cl


def fake_source_pull() -> list[dict]:
    """Replace with your real pull (API, file scan, export)."""
    return [
        {
            "id": "meet_001",
            "title": "Weekly sync",
            "participants": "Ana Souza, Bruno Lima",
            "text": "Ana will send the proposal by Friday. Bruno owns the deck.",
        },
        {
            "id": "meet_002",
            "title": "Client call — Acme",
            "participants": "Carla Reis",
            "text": "Acme wants a quote for the automation phase.",
        },
        {
            "id": "meet_003",
            "title": "1:1 review",
            "participants": "",
            "text": "",
        },
    ]


def main() -> int:
    added = skipped = 0
    for item in fake_source_pull():
        excerpt = item["text"] or item["title"]
        ok = cl.append_entry(
            source="meetings",                       # your producer id
            who=f"Meetings: {item['title']}" + (
                f" ({item['participants']})" if item["participants"] else ""
            ),
            excerpt=excerpt,
            ref=f"meetings:{item['id']}",            # deterministic ref
            who_kind="tool",
        )
        if ok:
            added += 1
        else:
            skipped += 1
    print(f"producer: added={added} skipped(dedupe)={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
