#!/usr/bin/env python3
"""Render two or three options side-by-side in the terminal with ANSI styling.

Usage:
    python3 render_options.py --input options.json [--cols 2|3] [--width N]
    cat options.json | python3 render_options.py [--cols 2|3]
    python3 render_options.py --demo

Input JSON shape:
    { "options": [ { "title": "...", "body": "..." }, ... ] }

`body` may include markdown fenced code blocks. Blocks tagged ```diff get per-line
coloring (green +, red -, blue @@ hunk headers, muted +++/--- file headers).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import textwrap

# 256-color ANSI
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
MUTED = "\033[38;5;245m"
ACCENT = "\033[38;5;75m"
BORDER = "\033[38;5;240m"
DIFF_ADD = "\033[38;5;114m"
DIFF_DEL = "\033[38;5;203m"
DIFF_HUNK = "\033[38;5;75m"
DIFF_META = "\033[38;5;245m"

ANSI_RE = re.compile(r"\033\[[0-9;]*m")


def visible_len(s: str) -> int:
    return len(ANSI_RE.sub("", s))


def pad_to(s: str, width: int) -> str:
    return s + " " * max(0, width - visible_len(s))


def truncate_to(s: str, width: int) -> str:
    if visible_len(s) <= width:
        return s
    plain = ANSI_RE.sub("", s)
    return plain[: max(0, width - 1)] + "…"


def colorize_diff_line(line: str) -> str:
    if line.startswith("+++") or line.startswith("---"):
        return f"{DIFF_META}{line}{RESET}"
    if line.startswith("+"):
        return f"{DIFF_ADD}{line}{RESET}"
    if line.startswith("-"):
        return f"{DIFF_DEL}{line}{RESET}"
    if line.startswith("@@"):
        return f"{DIFF_HUNK}{line}{RESET}"
    return line


def style_inline_code(text: str) -> str:
    return re.sub(r"`([^`]+)`", lambda m: f"{ACCENT}{m.group(1)}{RESET}", text)


def render_body(body: str, width: int) -> list[str]:
    out: list[str] = []
    in_fence = False
    fence_lang = ""
    for raw_line in body.split("\n"):
        stripped = raw_line.lstrip()
        if stripped.startswith("```"):
            if in_fence:
                in_fence = False
                fence_lang = ""
            else:
                in_fence = True
                lang = stripped.lstrip("`").strip()
                fence_lang = lang.lower() if lang else ""
            continue
        if in_fence:
            line = raw_line.rstrip("\n")
            if fence_lang.startswith("diff"):
                line = colorize_diff_line(line)
            else:
                line = f"{MUTED}{line}{RESET}"
            if visible_len(line) > width:
                line = truncate_to(line, width)
            out.append(line)
        else:
            line = style_inline_code(raw_line)
            wrapped = textwrap.wrap(
                line,
                width=width,
                break_long_words=False,
                break_on_hyphens=False,
                drop_whitespace=True,
            )
            if not wrapped:
                out.append("")
            else:
                out.extend(wrapped)
    return out


def detect_cols(opts_count: int, term_width: int) -> int:
    if opts_count <= 1:
        return 1
    if term_width >= 110 and opts_count >= 3:
        return 3
    return 2


def render(options: list[dict], cols: int | None, term_width: int | None) -> str:
    if term_width is None:
        term_width = shutil.get_terminal_size((120, 24)).columns

    if cols is None:
        cols = detect_cols(len(options), term_width)
    cols = max(1, min(cols, len(options)))

    gap = 2
    border_overhead = 4
    avail_for_content = term_width - gap * (cols - 1)
    col_outer = avail_for_content // cols
    inner_width = max(20, col_outer - border_overhead)

    columns = []
    for i in range(cols):
        opt = options[i] or {}
        title = str(opt.get("title", "(untitled)"))
        body = str(opt.get("body", ""))
        body_lines = render_body(body, inner_width)
        columns.append({"label": chr(ord("A") + i), "title": title, "lines": body_lines})

    body_height = max((len(c["lines"]) for c in columns), default=0)

    out_lines: list[str] = []

    top = []
    for c in columns:
        label = f"{ACCENT}{c['label']}{RESET}"
        title = f"{BOLD}{c['title']}{RESET}"
        prefix_styled = f"{BORDER}─ {RESET}{label}{BORDER} · {RESET}{title}{BORDER} "
        prefix_len = visible_len(prefix_styled)
        max_inner_with_borders = inner_width + 2
        if prefix_len > max_inner_with_borders:
            overflow = prefix_len - max_inner_with_borders
            short_title = c["title"]
            if len(short_title) > overflow + 1:
                short_title = short_title[: max(1, len(short_title) - overflow - 1)] + "…"
            else:
                short_title = "…"
            title = f"{BOLD}{short_title}{RESET}"
            prefix_styled = f"{BORDER}─ {RESET}{label}{BORDER} · {RESET}{title}{BORDER} "
            prefix_len = visible_len(prefix_styled)
        fill = max_inner_with_borders - prefix_len
        top.append(f"{BORDER}╭{prefix_styled}{'─' * fill}╮{RESET}")
    out_lines.append((" " * gap).join(top))

    for r in range(body_height):
        row = []
        for c in columns:
            content = c["lines"][r] if r < len(c["lines"]) else ""
            content = pad_to(content, inner_width)
            row.append(f"{BORDER}│{RESET} {content} {BORDER}│{RESET}")
        out_lines.append((" " * gap).join(row))

    bottom = [f"{BORDER}╰{'─' * (inner_width + 2)}╯{RESET}" for _ in columns]
    out_lines.append((" " * gap).join(bottom))

    labels = ", ".join(f"{ACCENT}{c['label']}{RESET}" for c in columns)
    out_lines.append(f"{MUTED}Pick one: {labels}{RESET}")

    return "\n".join(out_lines)


DEMO = {
    "options": [
        {
            "title": "Sum of last two",
            "body": (
                "Build the answer iteratively with two rolling vars. O(n) time, "
                "O(1) space. Maps directly to the recurrence f(n) = f(n-1) + f(n-2).\n\n"
                "```diff\n"
                "@@ -1,2 +1,5 @@\n"
                " def climb(n):\n"
                "-    pass\n"
                "+    a, b = 1, 1\n"
                "+    for _ in range(n):\n"
                "+        a, b = b, a + b\n"
                "+    return a\n"
                "```"
            ),
        },
        {
            "title": "Naive recursion",
            "body": (
                "Recurse directly on the definition. Elegant but exponential time.\n\n"
                "```diff\n"
                "@@ -1,2 +1,3 @@\n"
                " def climb(n):\n"
                "-    pass\n"
                "+    if n < 2: return 1\n"
                "+    return climb(n-1) + climb(n-2)\n"
                "```"
            ),
        },
        {
            "title": "Doubles each step",
            "body": (
                "Double the running count each step, since each step has two choices.\n\n"
                "```diff\n"
                "@@ -1,2 +1,2 @@\n"
                " def climb(n):\n"
                "-    pass\n"
                "+    return 2 ** n\n"
                "```"
            ),
        },
    ],
}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", "-i", default="-", help="JSON file path, or '-' for stdin (default)")
    p.add_argument("--cols", type=int, default=None, help="Force 2 or 3 columns (default auto)")
    p.add_argument("--width", type=int, default=None, help="Force terminal width")
    p.add_argument("--demo", action="store_true", help="Render built-in sample options")
    args = p.parse_args()

    if args.demo:
        data = DEMO
    elif args.input == "-":
        data = json.load(sys.stdin)
    else:
        with open(args.input) as f:
            data = json.load(f)

    options = data.get("options") or []
    if not options:
        print("No options to render.", file=sys.stderr)
        sys.exit(1)

    print(render(options, cols=args.cols, term_width=args.width))


if __name__ == "__main__":
    main()
