#!/usr/bin/env python3
"""Context Ledger — unified index of everything that reaches your agent.

Design locks (do not change without a real query demanding it):
1. A new field only enters when a real query requires it.
2. No interpretation at capture — excerpt is raw text; analysis happens at read time.

Schema (6 fixed fields):
  ts        ISO timestamp in the local timezone
  source    producer id (gmail | whatsapp | granola | fathom | calendar | ...)
  who       sender exactly as it arrived
  who_kind  person | tool | transactional | unknown
  excerpt   raw text truncated (~200 chars)
  ref       stable id for dedupe + tracing back to the original

Append-only; dedupe by ref; corrections are new rows.
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TZ_NAME = os.environ.get("CONTEXT_LEDGER_TZ", "America/Sao_Paulo")
TZ = ZoneInfo(TZ_NAME)
LEDGER_PATH = Path(
    os.environ.get("LEDGER_PATH", "context-ledger.jsonl")
)
EXCERPT_MAX = 200

# Tools and services: senders that are not people-in-relationship.
TOOL_DOMAINS = (
    "fathom", "granola", "notion", "slack", "github", "google", "gmail",
    "youtube", "instagram", "meta", "linkedin", "discord", "telegram",
    "stripe", "paypal", "mercadopago", "hotmart", "beehiiv", "substack",
    "replit", "vercel", "railway", "supabase", "hostinger", "cloudflare",
    "aws", "openai", "anthropic", "x.ai", "groq", "elevenlabs", "figma",
    "loom", "zoom", "meet", "calendly", "cal.com", "zapier", "n8n",
    "intercom", "crisp", "zendesk", "mailchimp", "brevo",
    "activecampaign", "convertkit", "hubspot", "salesforce", "asana",
    "clickup", "trello", "linear", "jira", "airtable", "whatsapp",
)
TOOL_SENDERS = ("noreply", "no-reply", "donotreply", "notify", "notification",
                "notifications", "alerts", "billing", "support", "team@",
                "hello@", "contato@", "do-not-reply")
# Transactional: logistics/finance — not a person, but not noise either.
# CHECKED FIRST (see lessons/01-classifier-order.md).
TRANSACTIONAL_DOMAINS = ("latam", "gol", "azul", "booking", "airbnb",
                         "expedia", "decolar", "maxmilhas", "itau", "bradesco",
                         "nubank", "inter", "banco", "receita", "gov.br",
                         "unimed", "seguro", "flytour", "alatur", "mapfre")

PERSON_HINT = re.compile(
    r"^[\wà-ú'’.-]+ [\wà-ú'’.-]+"  # two words separated = looks like a name
)


def now_local_iso() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def classify_who(who: str, domain: str = "") -> str:
    """Classify the sender: person | tool | transactional | unknown.

    Deterministic (denylists + heuristic), no LLM.
    Order matters: transactional first, so noreply@latam.com does not
    become a "tool".
    """
    text = f"{who} {domain}".lower()
    if any(d in text for d in TRANSACTIONAL_DOMAINS):
        return "transactional"
    if any(d in text for d in TOOL_SENDERS):
        return "tool"
    if any(d in text for d in TOOL_DOMAINS):
        return "tool"
    if "@" in (domain or ""):
        # has an email domain and matched nothing else → likely a person
        return "person"
    if PERSON_HINT.match(who.strip() or ""):
        return "person"
    return "unknown"


def clean_excerpt(text: str, limit: int = EXCERPT_MAX) -> str:
    t = re.sub(r"\s+", " ", text or "").strip()
    return t[:limit] + ("…" if len(t) > limit else "")


def load_refs(path: Path | None = None) -> set[str]:
    path = path or LEDGER_PATH
    refs: set[str] = set()
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                refs.add(json.loads(line).get("ref", ""))
            except Exception:
                continue
    return refs


def append_entry(source: str, who: str, excerpt: str, ref: str,
                 who_kind: str | None = None, ts: str | None = None,
                 path: Path | None = None) -> bool:
    """Append one normalized row. Returns False when ref already exists (dedupe).

    NOTE: load_refs() scans the whole file per write — fine up to ~100k rows
    (see lessons/05-growth.md). For larger volumes, keep refs in a sidecar set.
    """
    path = path or LEDGER_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    if ref and ref in load_refs(path):
        return False
    entry = {
        "ts": ts or now_local_iso(),
        "source": source,
        "who": who,
        "who_kind": who_kind or classify_who(who),
        "excerpt": clean_excerpt(excerpt),
        "ref": ref,
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return True


if __name__ == "__main__":
    # smoke test
    # Fictional identity using a reserved example domain.
    print(classify_who("Pessoa Exemplo", "pessoa@example.com"))              # person
    print(classify_who("Fathom", "noreply@fathom.video"))                    # tool
    print(classify_who("LATAM", "noreply@latam.com"))                        # transactional
    print(classify_who("Blueticket", ""))                                    # unknown
