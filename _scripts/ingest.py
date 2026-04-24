#!/usr/bin/env python3
"""
Guruji Knowledge Base → SQLite-vec ingestion.

Walks guruji-knowledge/, validates YAML frontmatter against the template
for each content_type, chunks the body, and writes to the memory.db.

Usage:
  python3 _scripts/ingest.py                 # ingest all
  python3 _scripts/ingest.py --dry-run       # validate only, no DB writes
  python3 _scripts/ingest.py --path <file>   # single file
  python3 _scripts/ingest.py --rebuild       # drop + re-ingest all kb rows
"""
import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Missing dependency: pip3 install pyyaml --break-system-packages", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "_templates"
DB_PATH = Path.home() / ".config" / "kiran-memory" / "memory.db"
LOG = ROOT / "_scripts" / "ingest.log"

REQUIRED_BY_TYPE = {
    "research-paper": ["paper_id", "title", "authority_level", "branch", "category"],
    "website-content": ["title", "url", "authority_level"],
    "blog-post": ["title", "authority_level", "status"],
    "testimonial": ["name", "date", "pillar_attribution"],
    "talk-transcript": ["title", "speaker", "date"],
    "religious-text": ["title", "tradition", "authority_level"],
}

AUTHORITY_LEVELS = {"primary", "official", "derivative", "draft"}
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)


def log(msg: str) -> None:
    stamp = datetime.now().isoformat(timespec="seconds")
    line = f"[{stamp}] {msg}"
    print(line)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(line + "\n")


def parse_file(path: Path):
    raw = path.read_text(encoding="utf-8")
    m = FM_RE.match(raw)
    if not m:
        return None, raw, "no frontmatter"
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        return None, raw, f"yaml error: {e}"
    return fm, m.group(2), None


def validate(fm: dict, path: Path):
    errs = []
    ct = fm.get("content_type")
    if not ct:
        errs.append("missing content_type")
        return errs
    if ct not in REQUIRED_BY_TYPE:
        errs.append(f"unknown content_type: {ct}")
        return errs
    for req in REQUIRED_BY_TYPE[ct]:
        if req not in fm or fm[req] in (None, ""):
            errs.append(f"missing required field: {req}")
    al = fm.get("authority_level")
    if al and al not in AUTHORITY_LEVELS:
        errs.append(f"invalid authority_level: {al}")
    # Mango safety gate
    if ct == "research-paper" and fm.get("paper_id") == "MKT-164":
        warnings = fm.get("warnings") or []
        if not any("DNA" in str(w) or "polymorphism" in str(w) for w in warnings):
            errs.append("MKT-164 must include DNA polymorphism warning (standing order 2026-04-04)")
    return errs


def chunk_body(body: str, target: int = 1200):
    """Paragraph-aware chunking, target ~1200 chars per chunk."""
    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    chunks, cur = [], ""
    for p in paras:
        if len(cur) + len(p) + 2 > target and cur:
            chunks.append(cur.strip())
            cur = p
        else:
            cur = (cur + "\n\n" + p) if cur else p
    if cur.strip():
        chunks.append(cur.strip())
    return chunks or [body.strip()]


def ensure_schema(con: sqlite3.Connection) -> None:
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS kb_docs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE NOT NULL,
            content_type TEXT NOT NULL,
            authority_level TEXT NOT NULL,
            title TEXT,
            frontmatter_json TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            ingested_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS kb_chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id INTEGER NOT NULL REFERENCES kb_docs(id) ON DELETE CASCADE,
            chunk_idx INTEGER NOT NULL,
            text TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_kb_chunks_doc ON kb_chunks(doc_id);
        CREATE INDEX IF NOT EXISTS idx_kb_docs_type ON kb_docs(content_type);
        """
    )
    con.commit()


def upsert(con: sqlite3.Connection, path: Path, fm: dict, body: str) -> bool:
    h = hashlib.sha256((json.dumps(fm, sort_keys=True, default=str) + body).encode()).hexdigest()
    rel = str(path.relative_to(ROOT))
    row = con.execute("SELECT id, content_hash FROM kb_docs WHERE path=?", (rel,)).fetchone()
    if row and row[1] == h:
        return False  # unchanged
    if row:
        con.execute("DELETE FROM kb_chunks WHERE doc_id=?", (row[0],))
        con.execute("DELETE FROM kb_docs WHERE id=?", (row[0],))
    cur = con.execute(
        "INSERT INTO kb_docs(path, content_type, authority_level, title, frontmatter_json, content_hash, ingested_at) VALUES(?,?,?,?,?,?,?)",
        (
            rel,
            fm.get("content_type", "unknown"),
            fm.get("authority_level", "draft"),
            fm.get("title", ""),
            json.dumps(fm, default=str),
            h,
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    doc_id = cur.lastrowid
    for i, c in enumerate(chunk_body(body)):
        con.execute(
            "INSERT INTO kb_chunks(doc_id, chunk_idx, text) VALUES(?,?,?)",
            (doc_id, i, c),
        )
    con.commit()
    return True


def walk(root: Path):
    for p in root.rglob("*.md"):
        parts = set(p.relative_to(root).parts)
        if parts & {"_templates", "_indexes", "_scripts"}:
            continue
        if p.name == "README.md":
            continue
        yield p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--path", type=str)
    ap.add_argument("--rebuild", action="store_true")
    args = ap.parse_args()

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    ensure_schema(con)

    if args.rebuild and not args.dry_run:
        con.execute("DELETE FROM kb_chunks")
        con.execute("DELETE FROM kb_docs")
        con.commit()
        log("rebuild: cleared kb_docs + kb_chunks")

    if args.path:
        p = Path(args.path).expanduser()
        if not p.is_absolute():
            p = (Path.cwd() / p).resolve()
        targets = [p]
    else:
        targets = list(walk(ROOT))
    ok, skip, err = 0, 0, 0
    for p in targets:
        fm, body, parse_err = parse_file(p)
        if parse_err:
            log(f"SKIP {p.relative_to(ROOT)} — {parse_err}")
            skip += 1
            continue
        errs = validate(fm, p)
        if errs:
            log(f"FAIL {p.relative_to(ROOT)} — {'; '.join(errs)}")
            err += 1
            continue
        if args.dry_run:
            log(f"OK   {p.relative_to(ROOT)} — validated")
            ok += 1
            continue
        changed = upsert(con, p, fm, body)
        log(f"{'INGEST' if changed else 'UNCHANGED'} {p.relative_to(ROOT)}")
        ok += 1

    log(f"done — ok={ok} skip={skip} err={err} dry_run={args.dry_run}")
    con.close()
    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main()
