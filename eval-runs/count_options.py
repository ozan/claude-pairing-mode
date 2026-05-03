#!/usr/bin/env python3
"""Count `propose_options` events across one or more transcript runs.

Usage:
  ./count_options.py                       # all collections under .
  ./count_options.py 20260502-182951       # one collection
  ./count_options.py path/to/transcript.jsonl   # one transcript
"""

import json
import sys
from pathlib import Path


def count_in(transcript: Path) -> int:
    n = 0
    with transcript.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("kind") == "pair_event_with_notes":
                n += 1
    return n


def main() -> None:
    target = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent)

    if target.is_file():
        n = count_in(target)
        print(f"{target}: {n}")
        return

    transcripts = sorted(target.rglob("transcript.jsonl"))
    if not transcripts:
        print(f"No transcripts found under {target}", file=sys.stderr)
        sys.exit(1)

    total = 0
    by_collection: dict[str, int] = {}
    for t in transcripts:
        n = count_in(t)
        total += n
        rel = t.relative_to(target)
        # rel is like <collection>/<slug>/transcript.jsonl when target is eval-runs
        # or <slug>/transcript.jsonl when target is one collection.
        parts = rel.parts
        if len(parts) >= 3:
            collection = parts[0]
            slug = parts[1]
            label = f"{collection}/{slug}"
        else:
            collection = "."
            slug = parts[0]
            label = slug
        by_collection[collection] = by_collection.get(collection, 0) + n
        print(f"  {label}: {n}")

    if len(by_collection) > 1:
        print()
        print("Per collection:")
        for c, n in sorted(by_collection.items()):
            print(f"  {c}: {n}")
    print()
    print(f"Total: {total} option presentations across {len(transcripts)} run(s)")


if __name__ == "__main__":
    main()
