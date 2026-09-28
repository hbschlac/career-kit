#!/usr/bin/env python3
"""Leak check: fail if personal data shows up anywhere outside profile/.

Everything personal belongs in profile/ (your resume, facts, voice, contacts, sheet IDs). The
skills, scripts and docs must stay generic so the kit can be shared. This scans every tracked
text file except profile/ for things that identify a real person:

  - email addresses (except @example.com / @example.org and no-reply senders)
  - US-style phone numbers
  - Google Doc / Sheet / Drive IDs (the 25-44 char tokens in docs.google.com URLs)
  - any regex in a denylist file (--denylist PATH), one per line, case-insensitive

Usage:
  python3 scripts/leak_check.py                 # scan this repo
  python3 scripts/leak_check.py PATH            # scan another checkout
  python3 scripts/leak_check.py --denylist my-names.txt
Exit 0 = clean, 1 = findings (printed as path:line: match).
"""
import argparse, pathlib, re, sys

SKIP_DIRS = {".git", "profile", "__pycache__", "node_modules"}
TEXT_EXT = {".md", ".MD", ".py", ".sh", ".json", ".txt", ".yml", ".yaml", ".csv", ".toml", ""}
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
EMAIL_OK = re.compile(r"@(example\.(com|org)|users\.noreply\.github\.com|anthropic\.com$)|^no-?reply@|^noreply@", re.I)
PHONE = re.compile(r"(?<![\d.])\(?\b\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b")
GOOGLE_ID = re.compile(r"(?<![A-Za-z0-9_-])1[A-Za-z0-9_-]{24,43}(?![A-Za-z0-9_-])")
GOOGLE_ID_OK = re.compile(r"^1[a-z_]+$|^1X{10,}")  # plain words / placeholders


def load_denylist(path):
    pats = []
    for raw in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if s and not s.startswith("#"):
            pats.append((s, re.compile(s, re.I if s == s.lower() or not s[:1].isupper() else 0)))
    return pats


def files(root):
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts) or not p.is_file() or p.is_symlink():
            continue
        if p.suffix in TEXT_EXT and p.name != "leak_check.py":
            yield p, rel


def scan(root, deny):
    hits = []
    for p, rel in files(root):
        try:
            lines = p.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(lines, 1):
            for m in EMAIL.finditer(line):
                if not EMAIL_OK.search(m.group(0)):
                    hits.append((rel, n, "email", m.group(0)))
            for m in PHONE.finditer(line):
                hits.append((rel, n, "phone", m.group(0)))
            for m in GOOGLE_ID.finditer(line):
                tok = m.group(0)
                if not GOOGLE_ID_OK.search(tok) and re.search(r"\d", tok[1:]) and re.search(r"[A-Z]", tok):
                    hits.append((rel, n, "google-id", tok))
            for src, rx in deny:
                m = rx.search(line)
                if m:
                    hits.append((rel, n, f"denylist /{src}/", m.group(0)))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default=str(pathlib.Path(__file__).resolve().parent.parent))
    ap.add_argument("--denylist")
    a = ap.parse_args()
    root = pathlib.Path(a.path).resolve()
    hits = scan(root, load_denylist(a.denylist) if a.denylist else [])
    for rel, n, kind, what in hits:
        print(f"{rel}:{n}: {kind}: {what}")
    print(f"leak_check: {len(hits)} finding(s) in {root}" if hits else f"leak_check: clean ({root})")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
