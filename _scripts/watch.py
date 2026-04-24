#!/usr/bin/env python3
"""
Watch guruji-knowledge/ for changes and auto-ingest.
Polls every 3s (no extra deps). For heavy use, swap to watchdog later.
"""
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INGEST = Path(__file__).resolve().parent / "ingest.py"


def snapshot():
    state = {}
    for p in ROOT.rglob("*.md"):
        parts = set(p.relative_to(ROOT).parts)
        if parts & {"_templates", "_indexes", "_scripts"}:
            continue
        try:
            state[str(p)] = p.stat().st_mtime
        except FileNotFoundError:
            pass
    return state


def main():
    print(f"[watch] {ROOT}")
    last = snapshot()
    while True:
        time.sleep(3)
        cur = snapshot()
        changed = [p for p, m in cur.items() if last.get(p) != m]
        removed = [p for p in last if p not in cur]
        if changed or removed:
            print(f"[watch] {len(changed)} changed, {len(removed)} removed")
            for p in changed:
                subprocess.run(["python3", str(INGEST), "--path", p], check=False)
            if removed:
                # any removals trigger full re-ingest to clean orphaned rows
                subprocess.run(["python3", str(INGEST)], check=False)
            last = cur


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[watch] stopped")
