#!/usr/bin/env python3
"""Check local Markdown link targets and basic document hygiene, offline.

Not a complete secret scanner: manual privacy review remains mandatory.
Checks inline links used by this repository; not an arbitrary Markdown parser.
"""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "private host path": re.compile(r"/root/(?:workspace|\.hermes|second-brains|okamoto|worktrees)"),
    "private key": re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    "credential-shaped token": re.compile(r"\b(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{24,}|xox[baprs]-[A-Za-z0-9-]{20,})"),
}


def main():
    files = [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md")),
             *sorted((ROOT / "templates").glob("*.md"))]
    problems = []
    links = 0
    for path in files:
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            problems.append(f"{path.relative_to(ROOT)}: empty file")
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                problems.append(f"{path.relative_to(ROOT)}: {label}")
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", text):
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#"):
                continue
            links += 1
            local = (path.parent / unquote(parsed.path)).resolve()
            if not local.is_relative_to(ROOT) or not local.exists():
                problems.append(f"{path.relative_to(ROOT)}: broken/escaping link: {target}")
    if problems:
        print("FAIL\n" + "\n".join(problems))
        return 1
    print(f"PASS: {len(files)} documents, {links} local link targets; basic hygiene clean.")
    print("Scope: paths only, not heading anchors or external URLs; not a full secret audit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
