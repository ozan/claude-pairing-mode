#!/usr/bin/env python3
"""Aggregate grades across one or more collections.

Usage:
  ./aggregate_grades.py 003-baseline 004-initial    # side-by-side
  ./aggregate_grades.py 004-initial                 # one collection
"""

import json
import sys
from pathlib import Path

CRITERIA = [
    ("question_frequency", "pedagogical"),
    ("question_quality", "pedagogical"),
    ("scaffolding", "pedagogical"),
    ("flow_and_tone", "pedagogical"),
    ("effectiveness", "productivity"),
    ("friction", "productivity"),
]


def load_grades(collection_dir: Path) -> dict[str, dict]:
    """slug -> grade.json dict, missing slugs omitted."""
    out = {}
    for d in sorted(collection_dir.iterdir()):
        if not d.is_dir():
            continue
        gp = d / "grade.json"
        if not gp.exists():
            continue
        with gp.open() as f:
            out[d.name] = json.load(f)
    return out


def column(value, width):
    s = f"{value:.2f}" if isinstance(value, float) else str(value)
    return s.rjust(width)


def get_final(g: dict) -> float:
    """Read finalScore, falling back to (weightedScore − 1) / 4 for older grades."""
    if "finalScore" in g:
        return g["finalScore"]
    w = g.get("weightedScore", 0.0)
    return (w - 1) / 4 if w else 0.0


def print_collection(name: str, grades: dict[str, dict]) -> None:
    if not grades:
        print(f"\n## {name}: no grades found")
        return

    print(f"\n## {name} ({len(grades)} runs)\n")
    header = ["slug".ljust(28)] + [k[:5].rjust(5) for k, _ in CRITERIA] + ["wtd".rjust(5), "final".rjust(6)]
    print("  " + " ".join(header))
    sums = {k: 0.0 for k, _ in CRITERIA}
    wsum = 0.0
    fsum = 0.0
    for slug, g in grades.items():
        row = [slug[:28].ljust(28)]
        for k, group in CRITERIA:
            score = g[group][k]["score"]
            row.append(column(score, 5))
            sums[k] += score
        w = g.get("weightedScore", 0.0)
        f = get_final(g)
        wsum += w
        fsum += f
        row.append(column(w, 5))
        row.append(column(f, 6))
        print("  " + " ".join(row))

    avg_row = ["AVG".ljust(28)]
    for k, _ in CRITERIA:
        avg_row.append(column(sums[k] / len(grades), 5))
    avg_row.append(column(wsum / len(grades), 5))
    avg_row.append(column(fsum / len(grades), 6))
    print("  " + " ".join(avg_row))


def print_diff(left_name: str, left: dict, right_name: str, right: dict) -> None:
    """For each slug present in both, show right - left per criterion."""
    common = sorted(set(left) & set(right))
    if not common:
        return
    print(f"\n## delta: {right_name} − {left_name} ({len(common)} runs)\n")
    header = ["slug".ljust(28)] + [k[:5].rjust(6) for k, _ in CRITERIA] + ["wtd".rjust(6), "final".rjust(7)]
    print("  " + " ".join(header))
    sums = {k: 0.0 for k, _ in CRITERIA}
    wsum = 0.0
    fsum = 0.0
    for slug in common:
        l, r = left[slug], right[slug]
        row = [slug[:28].ljust(28)]
        for k, group in CRITERIA:
            d = r[group][k]["score"] - l[group][k]["score"]
            sums[k] += d
            sign = "+" if d > 0 else ""
            row.append(f"{sign}{d:.1f}".rjust(6))
        wd = r.get("weightedScore", 0) - l.get("weightedScore", 0)
        wsum += wd
        sign = "+" if wd > 0 else ""
        row.append(f"{sign}{wd:.2f}".rjust(6))
        fd = get_final(r) - get_final(l)
        fsum += fd
        sign = "+" if fd > 0 else ""
        row.append(f"{sign}{fd:.2f}".rjust(7))
        print("  " + " ".join(row))
    avg_row = ["AVG".ljust(28)]
    for k, _ in CRITERIA:
        d = sums[k] / len(common)
        sign = "+" if d > 0 else ""
        avg_row.append(f"{sign}{d:.2f}".rjust(6))
    d = wsum / len(common)
    sign = "+" if d > 0 else ""
    avg_row.append(f"{sign}{d:.2f}".rjust(6))
    fd = fsum / len(common)
    sign = "+" if fd > 0 else ""
    avg_row.append(f"{sign}{fd:.2f}".rjust(7))
    print("  " + " ".join(avg_row))


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    base = Path(__file__).parent
    collections = []
    for arg in sys.argv[1:]:
        p = (base / arg) if not Path(arg).is_absolute() else Path(arg)
        if not p.exists():
            print(f"not found: {p}", file=sys.stderr)
            sys.exit(1)
        collections.append((p.name, load_grades(p)))

    for name, grades in collections:
        print_collection(name, grades)

    if len(collections) == 2:
        print_diff(collections[0][0], collections[0][1], collections[1][0], collections[1][1])


if __name__ == "__main__":
    main()
