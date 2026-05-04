"""Bundle every run × problem under runs/ into a single browsable HTML SPA.

  uv run generate_viewer.py
  uv run generate_viewer.py -o /tmp/viewer.html

Produces eval_viewer.html (default) at the repo root level — a single
self-contained file with:
  - A heatmap matrix (rows = problems, cols = runs) showing each cell's
    normalized grade (color-coded). Click a cell to load that transcript.
  - A detail pane that renders the selected transcript with the same TUI-
    inspired styling described below.

Per-transcript rendering vocabulary, borrowed from the TUI
(tui/src/core/components/):
  - `⏺` marker for tutor text (Entries.tsx AssistantBlock)
  - `❯` marker for student replies (Entries.tsx UserLine)
  - `● ToolName(args)` head with green dot, `└ summary` continuation
    (Entries.tsx ToolPillRunning, ToolResult)
  - `● Update(file.py)` with `Added N, removed M lines` for Edit;
    `● Write(file.py)` with `Wrote N lines` for Write
  - Side-by-side rounded-border option boxes (OptionsBlock.tsx)
  - Diff coloring: `+` green on dark-green BG, `-` red on dark-red BG,
    hunk headers blue (Diff.tsx HUNK_FG/ADD_FG/DEL_FG)
  - Thinking blocks rendered collapsed
  - propose_options private notes (best_letter, rationale) collapsed under
    a "Private" disclosure — visible to a human reviewer, never to the student

Architecture: every transcript body is embedded as a hidden <div>; JS just
toggles visibility on click. No fetch, no server, no build step. ~5-10 MB
HTML for a full 5-run × 36-problem bundle, well within browser limits.

Skips run dirs starting with "_" (smoke runs).
"""

import argparse
import html
import json
import re
import sys
import time
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).parent.parent
RUNS_DIR = Path(__file__).parent / "runs"
PROBLEMS_PATH = Path(__file__).parent / "problems.json"

# Conditions that should always appear first, in this order, regardless of
# directory creation time. Anything else is sorted by mtime after these.
PINNED_TAGS = ("baseline", "learning", "initial")

FULL_PROPOSE_TOOL_NAME = "mcp__pairing__propose_options"
HIDDEN_TOOL_NAMES = {"ToolSearch"}

PEDAGOGICAL_KEYS = ("question_frequency", "question_quality", "scaffolding", "flow_and_tone")
PRODUCTIVITY_KEYS = ("effectiveness", "friction")


# ============================================================================
# Per-transcript rendering (markdown, diff, content blocks, turns, grade)
# ============================================================================

# ---------- minimal markdown (paragraphs, fenced code, inline) ----------

FENCE_RE = re.compile(r"```([a-zA-Z0-9_+\-]*)\n(.*?)```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
ITALIC_RE = re.compile(r"(?<![*\w])\*([^*\n]+)\*(?!\*)")


def _render_inline(s: str) -> str:
    s = html.escape(s)
    s = INLINE_CODE_RE.sub(lambda m: f"<code>{m.group(1)}</code>", s)
    s = BOLD_RE.sub(r"<strong>\1</strong>", s)
    s = ITALIC_RE.sub(r"<em>\1</em>", s)
    return s


def _render_paragraphs(s: str) -> str:
    chunks = [c.strip() for c in re.split(r"\n\s*\n", s) if c.strip()]
    return "\n".join(f"<p>{_render_inline(c)}</p>" for c in chunks)


def render_markdown(s: str) -> str:
    parts: list[str] = []
    last = 0
    for m in FENCE_RE.finditer(s):
        prose = s[last:m.start()]
        if prose.strip():
            parts.append(_render_paragraphs(prose))
        lang = m.group(1) or ""
        code = m.group(2)
        if lang == "diff":
            parts.append(_render_diff(code))
        elif lang:
            parts.append(f'<pre><code class="language-{lang}">{html.escape(code)}</code></pre>')
        else:
            parts.append(f'<pre><code>{html.escape(code)}</code></pre>')
        last = m.end()
    tail = s[last:]
    if tail.strip():
        parts.append(_render_paragraphs(tail))
    return "\n".join(parts)


# ---------- unified-diff renderer (mirrors Diff.tsx coloring) ----------

HUNK_RE = re.compile(r"^@@ -(\d+),?\d* \+(\d+),?\d* @@")


def _render_diff(raw: str) -> str:
    """Render a unified diff with TUI-style coloring. Hunk headers blue,
    `+` lines on dark-green BG, `-` lines on dark-red BG, context dim."""
    out = ['<pre class="diff">']
    new_num: int | None = None
    old_num: int | None = None
    for line in raw.split("\n"):
        if line.startswith("@@"):
            m = HUNK_RE.match(line)
            if m:
                old_num = int(m.group(1))
                new_num = int(m.group(2))
            out.append(f'<span class="diff-hunk">{html.escape(line)}</span>')
        elif line.startswith("+++") or line.startswith("---"):
            out.append(f'<span class="diff-meta">{html.escape(line)}</span>')
        elif line.startswith("+"):
            num = f"{new_num:>4} " if new_num is not None else "     "
            if new_num is not None:
                new_num += 1
            out.append(f'<span class="diff-add"><span class="diff-num">{num}</span>+ {html.escape(line[1:])}</span>')
        elif line.startswith("-"):
            num = f"{old_num:>4} " if old_num is not None else "     "
            if old_num is not None:
                old_num += 1
            out.append(f'<span class="diff-del"><span class="diff-num">{num}</span>- {html.escape(line[1:])}</span>')
        else:
            num = f"{new_num:>4} " if new_num is not None else "     "
            if new_num is not None:
                new_num += 1
            if old_num is not None:
                old_num += 1
            body = line[1:] if line.startswith(" ") else line
            out.append(f'<span class="diff-ctx"><span class="diff-num">{num}</span>  {html.escape(body)}</span>')
    out.append("</pre>")
    # Join with "" not "\n": each span has display:block so it makes its own
    # line. A literal newline inside <pre> would render as an EXTRA blank
    # line on top of that, double-spacing the whole diff.
    return "".join(out)


# ---------- TUI-style tool helpers ----------

def _summarize_input(name: str, args: dict[str, Any]) -> str:
    """Mirror Entries.tsx summarizeInput."""
    if not args:
        return ""
    for key in ("command", "file_path", "path", "pattern", "url", "prompt", "query"):
        v = args.get(key)
        if isinstance(v, str):
            return v if len(v) <= 80 else v[:80] + "…"
    return ""


def _short_tool_name(name: str) -> str:
    """Mirror Entries.tsx shortToolName: strip mcp__ prefix, rename Edit→Update."""
    if not name:
        return "tool"
    raw = name.replace("mcp__", "")
    if "__" in raw:
        raw = raw.split("__")[-1]
    if raw == "Edit":
        return "Update"
    return raw


def _line_diff(old: str, new: str) -> tuple[int, int]:
    """Crude per-line diff returning (added, removed) counts."""
    a = old.split("\n")
    b = new.split("\n")
    common = set(a) & set(b)
    return (sum(1 for l in b if l not in common),
            sum(1 for l in a if l not in common))


# ---------- block detection (field-shape based, no __type__ dependency) ----------

def _block_kind(b: dict) -> str:
    """Detect content block kind by field shape. dataclasses.asdict() strips
    __type__ from nested dataclasses, so we have to discriminate structurally."""
    if "thinking" in b:
        return "thinking"
    if "name" in b and "input" in b:
        return "tool_use"
    if "tool_use_id" in b:
        return "tool_result"
    if "text" in b:
        return "text"
    return "?"


def _msg_kind(m: dict) -> str:
    """Detect SDK message kind. The top-level __type__ IS preserved for messages
    by run.py's _serialize, but we fall back to shape detection in case."""
    t = m.get("__type__")
    if t in ("AssistantMessage", "UserMessage", "SystemMessage", "ResultMessage"):
        return t
    if "subtype" in m:
        return "SystemMessage"
    if "duration_ms" in m:
        return "ResultMessage"
    if "content" in m and isinstance(m.get("content"), list):
        for b in m["content"]:
            if isinstance(b, dict) and ("name" in b and "input" in b):
                return "AssistantMessage"
            if isinstance(b, dict) and "text" in b and "tool_use_id" not in b:
                return "AssistantMessage"
        return "UserMessage"
    return "?"


# ---------- per-block render ----------

def _render_thinking(text: str) -> str:
    return (
        '<details class="thinking">'
        '<summary>thinking…</summary>'
        f'<div class="thinking-body">{html.escape(text)}</div>'
        '</details>'
    )


def _render_assistant_text(text: str) -> str:
    return (
        '<div class="assistant">'
        '<span class="marker">⏺</span>'
        f'<div class="assistant-body">{render_markdown(text)}</div>'
        '</div>'
    )


def _render_tool_pill(name: str, inp: dict, result: dict | None) -> str:
    """`● Name(args)` head + `└ summary` continuation. For Edit/Write, includes
    the diff body. result is {"text": str, "isError": bool} or None."""
    short = _short_tool_name(name)
    args = _summarize_input(name, inp)
    is_error = bool(result and result.get("isError"))
    dot_class = "dot-error" if is_error else "dot-done"

    head = (
        f'<div class="tool-head">'
        f'<span class="dot {dot_class}">●</span> '
        f'<span class="tool-name">{html.escape(short)}</span>'
        f'{("<span>(" + html.escape(args) + ")</span>") if args else ""}'
        f'</div>'
    )

    # Edit (TUI calls this Update): show old → new as a synthesized diff.
    if short == "Update":
        old = str(inp.get("old_string", ""))
        new = str(inp.get("new_string", ""))
        added, removed = _line_diff(old, new)
        summary = f'Added <strong>{added}</strong> line{"s" if added != 1 else ""}'
        if removed:
            summary += f', removed <strong>{removed}</strong> line{"s" if removed != 1 else ""}'
        diff_lines = []
        for l in old.split("\n"):
            if l:
                diff_lines.append(f'<span class="diff-del"><span class="diff-num">     </span>- {html.escape(l)}</span>')
        for l in new.split("\n"):
            if l:
                diff_lines.append(f'<span class="diff-add"><span class="diff-num">     </span>+ {html.escape(l)}</span>')
        diff_html = '<pre class="diff">' + "".join(diff_lines) + '</pre>'
        return (
            '<div class="tool">'
            f'{head}'
            f'<div class="tool-cont">└ {summary}</div>'
            f'{diff_html}'
            '</div>'
        )

    if short == "Write":
        content = str(inp.get("content", ""))
        n_lines = len(content.split("\n")) if content else 0
        summary = f'Wrote <strong>{n_lines}</strong> line{"s" if n_lines != 1 else ""}'
        diff_lines = []
        for l in content.split("\n"):
            diff_lines.append(f'<span class="diff-add"><span class="diff-num">     </span>+ {html.escape(l)}</span>')
        diff_html = '<pre class="diff">' + "".join(diff_lines) + '</pre>'
        return (
            '<div class="tool">'
            f'{head}'
            f'<div class="tool-cont">└ {summary}</div>'
            f'{diff_html}'
            '</div>'
        )

    # Other tools: just `└ <summary>` based on result text.
    cont = ""
    if result is not None:
        text = (result.get("text") or "").strip()
        if is_error:
            first = text.split("\n")[0] if text else "Error"
            cont = f'<div class="tool-cont err">└ {html.escape(first[:200])}</div>'
        elif short in ("Bash", "Glob", "Grep") and text:
            lines = [l for l in text.split("\n") if l]
            if len(lines) <= 1:
                t = lines[0] if lines else ""
                cont = f'<div class="tool-cont">└ {html.escape(t[:200])}</div>'
            else:
                visible = lines[:10]
                rem = len(lines) - len(visible)
                items = "<br>".join("&nbsp;&nbsp;" + html.escape(l[:200]) for l in visible)
                tail = f'<br>&nbsp;&nbsp;… <strong>{rem}</strong> more line{"s" if rem != 1 else ""}' if rem else ""
                cont = f'<div class="tool-cont">└ {items}{tail}</div>'
        elif short == "Read":
            n = len([l for l in text.split("\n") if l])
            cont = f'<div class="tool-cont">└ Read <strong>{n}</strong> line{"s" if n != 1 else ""}</div>'
        else:
            n = len([l for l in text.split("\n") if l])
            label = "ok" if not n else f'<strong>{n}</strong> line{"s" if n != 1 else ""}'
            cont = f'<div class="tool-cont">└ {label}</div>'

    return f'<div class="tool">{head}{cont}</div>'


def _render_options_block(inp: dict) -> str:
    """Side-by-side A/B boxes with rounded border, plus a collapsed Private
    section with best_letter and rationale."""
    a_t = html.escape(str(inp.get("option_a_title", "")))
    a_b = render_markdown(str(inp.get("option_a_body", "")))
    b_t = html.escape(str(inp.get("option_b_title", "")))
    b_b = render_markdown(str(inp.get("option_b_body", "")))
    best = str(inp.get("best_letter", ""))
    rationale = html.escape(str(inp.get("rationale", "")))
    a_class = "opt" + (" opt-best" if best == "A" else "")
    b_class = "opt" + (" opt-best" if best == "B" else "")
    return (
        '<div class="options">'
        f'<div class="{a_class}"><div class="opt-title">A.&nbsp;&nbsp;{a_t}</div><div class="opt-body">{a_b}</div></div>'
        f'<div class="{b_class}"><div class="opt-title">B.&nbsp;&nbsp;{b_t}</div><div class="opt-body">{b_b}</div></div>'
        '</div>'
        '<details class="private">'
        f'<summary>private (best=<strong>{html.escape(best)}</strong>)</summary>'
        f'<div class="private-body">{rationale}</div>'
        '</details>'
    )


def _result_payload(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(c.get("text", "") for c in content if isinstance(c, dict))
    return ""


def _render_tutor_turn(messages: list[dict]) -> str:
    """Walk per-turn messages in document order. Defer tool_use rendering until
    its result arrives so we can render `head` + `└ summary` together."""
    out: list[str] = []
    pending_tool: dict[str, dict] = {}  # tool_use_id -> {"name", "input", "idx"}

    for m in messages:
        kind = _msg_kind(m)
        if kind == "AssistantMessage":
            for block in m.get("content", []):
                if not isinstance(block, dict):
                    continue
                bk = _block_kind(block)
                if bk == "thinking":
                    text = block.get("thinking", "").strip()
                    if text:
                        out.append(_render_thinking(text))
                elif bk == "text":
                    text = (block.get("text") or "").strip()
                    if text:
                        out.append(_render_assistant_text(text))
                elif bk == "tool_use":
                    name = block.get("name", "")
                    inp = block.get("input", {})
                    if name in HIDDEN_TOOL_NAMES:
                        continue
                    if name == FULL_PROPOSE_TOOL_NAME:
                        out.append(_render_options_block(inp))
                    else:
                        idx = len(out)
                        out.append("")
                        pending_tool[block.get("id", "")] = {"name": name, "input": inp, "idx": idx}
        elif kind == "UserMessage":
            content = m.get("content", [])
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict):
                    continue
                if _block_kind(block) == "tool_result":
                    tid = block.get("tool_use_id", "")
                    text = _result_payload(block.get("content"))
                    rec = pending_tool.pop(tid, None)
                    if rec:
                        out[rec["idx"]] = _render_tool_pill(
                            rec["name"], rec["input"],
                            {"text": text, "isError": bool(block.get("is_error"))},
                        )

    # Tool uses without a matching result: render anyway.
    for tid, rec in pending_tool.items():
        out[rec["idx"]] = _render_tool_pill(rec["name"], rec["input"], None)

    return "\n".join(x for x in out if x)


def _render_student_turn(text: str) -> str:
    return (
        '<div class="user">'
        '<span class="marker user-marker">❯</span>'
        f'<div class="user-body">{render_markdown(text)}</div>'
        '</div>'
    )


# ---------- grade card ----------

def _score_class(score: float) -> str:
    if score >= 4: return "score-hi"
    if score >= 3: return "score-mid"
    return "score-lo"


def _render_grade(grade_path: Path) -> str:
    """Read grade.json and render the per-criterion verdicts as a card.
    Returns "" if no grade.json present."""
    if not grade_path.exists():
        return ""
    try:
        g = json.loads(grade_path.read_text())
    except Exception:
        return ""
    grade = g.get("grade", {})
    weighted = g.get("weighted", 0)
    normalized = g.get("normalized", 0)

    rows = []
    for cat_label, keys, cat_class in (
        ("PEDAGOGICAL", PEDAGOGICAL_KEYS, "ped"),
        ("PRODUCTIVITY", PRODUCTIVITY_KEYS, "prod"),
    ):
        cat = grade.get(cat_label.lower(), {})
        rows.append(f'<tr class="grade-cat"><td colspan="3">{cat_label}</td></tr>')
        for k in keys:
            v = cat.get(k, {})
            score = v.get("score", "?")
            rationale = html.escape(str(v.get("rationale", "")))
            score_cls = _score_class(score) if isinstance(score, (int, float)) else ""
            rows.append(
                f'<tr class="grade-row {cat_class}">'
                f'<td class="grade-name">{k.replace("_", " ")}</td>'
                f'<td class="grade-score"><span class="score-badge {score_cls}">{score}</span></td>'
                f'<td class="grade-rationale">{rationale}</td>'
                '</tr>'
            )

    return (
        '<details class="grade" open>'
        f'<summary>grade · weighted <strong>{weighted:.2f}</strong>/5 · normalized <strong>{normalized:.2f}</strong>/1</summary>'
        f'<table class="grade-table"><tbody>{"".join(rows)}</tbody></table>'
        '</details>'
    )


# ---------- assemble one transcript body ----------

def render_transcript_body(jsonl_path: Path) -> str:
    """Render the inner body of a transcript (no <html>/<head>/<style>).
    Embedded as a hidden panel in the SPA's right pane."""
    records = [json.loads(line) for line in jsonl_path.read_text().splitlines() if line.strip()]

    run_start = next((r for r in records if r["kind"] == "run_start"), None)
    run_end = next((r for r in records if r["kind"] == "run_end"), None)

    msgs_by_turn: dict[int, list[dict]] = {}
    student_by_turn: dict[int, str] = {}
    leaks_by_turn: dict[int, list] = {}
    for r in records:
        k = r["kind"]
        if k == "tutor_message":
            msgs_by_turn.setdefault(r["turn"], []).append(r["message"])
        elif k == "student_reply":
            student_by_turn[r["turn"]] = r["text"]
        elif k == "leak_detected":
            leaks_by_turn.setdefault(r["turn"], []).extend(r["leaks"])

    turns_html = []
    for turn in sorted(msgs_by_turn):
        tutor_html = _render_tutor_turn(msgs_by_turn[turn])
        leaks = leaks_by_turn.get(turn, [])
        leak_html = "".join(f'<div class="leak">LEAK: {html.escape(str(x))}</div>' for x in leaks)
        student_text = student_by_turn.get(turn, "")
        student_html = _render_student_turn(student_text) if student_text else ""
        turns_html.append(
            f'<div class="turn"><div class="turn-header">turn {turn}</div>'
            f'{tutor_html}{leak_html}{student_html}'
            f'</div>'
        )

    slug = run_start["problem"]["slug"] if run_start else jsonl_path.parent.name
    cond = run_start.get("condition", "?") if run_start else "?"
    tutor_m = run_start.get("tutor_model", "?") if run_start else "?"
    student_m = run_start.get("student_model", "?") if run_start else "?"
    prompt = run_start["problem"].get("prompt", "") if run_start else ""

    footer = ""
    if run_end:
        footer = (
            f"run end: <strong>{run_end.get('reason', '?')}</strong> · "
            f"{run_end.get('turns', 0)} turn(s) · "
            f"{run_end.get('duration_s', 0):.1f}s"
        )

    grade_html = _render_grade(jsonl_path.parent / "grade.json")

    return (
        f'<h1>{html.escape(slug)}</h1>'
        f'<div class="meta"><span class="mono">{html.escape(cond)}</span> · '
        f'tutor <span class="mono">{html.escape(tutor_m)}</span> · '
        f'student <span class="mono">{html.escape(student_m)}</span></div>'
        + grade_html
        + f'<h2>initial prompt</h2><div class="problem-prompt">{_render_inline(prompt)}</div>'
        + "".join(turns_html)
        + f'<div class="meta" style="margin-top:24px;">{footer}</div>'
    )


# ============================================================================
# SPA — discovery, matrix, panels, controls
# ============================================================================

def _score_color(score: float | None) -> str:
    """Heatmap cell background. Coordinates with the score-badge palette."""
    if score is None:
        return "#1a1a1a"
    if score >= 0.85: return "#0a3d0a"
    if score >= 0.7:  return "#0a4d0a"
    if score >= 0.55: return "#3d3a0a"
    if score >= 0.4:  return "#3d2a0a"
    return "#3d0a0a"


def _score_text_color(score: float | None) -> str:
    if score is None:
        return "#444"
    if score >= 0.55: return "#a0e0a0"
    return "#e0a0a0"


def _discover_runs(runs_dir: Path) -> list[dict[str, Any]]:
    """Return list of {tag, condition, problems, summary, mean_normalized},
    sorted with PINNED_TAGS first (in declared order) and the rest by
    directory mtime ascending. Skips dirs starting with '_' and any without
    config.json."""
    out = []
    for tag_dir in runs_dir.iterdir():
        if not tag_dir.is_dir() or tag_dir.name.startswith("_"):
            continue
        cfg_path = tag_dir / "config.json"
        if not cfg_path.exists():
            continue
        try:
            cfg = json.loads(cfg_path.read_text())
        except Exception:
            continue
        summary_path = tag_dir / "grades_summary.json"
        summary = json.loads(summary_path.read_text()) if summary_path.exists() else None
        problems = []
        for sub in sorted(tag_dir.iterdir()):
            if not sub.is_dir():
                continue
            jsonl = sub / "transcript.jsonl"
            if not jsonl.exists():
                continue
            grade_path = sub / "grade.json"
            grade = None
            if grade_path.exists():
                try:
                    grade = json.loads(grade_path.read_text())
                except Exception:
                    pass
            problems.append({
                "slug": sub.name,
                "jsonl": jsonl,
                "normalized": grade.get("normalized") if grade else None,
                "weighted": grade.get("weighted") if grade else None,
            })
        out.append({
            "tag": tag_dir.name,
            "condition": cfg.get("condition", "?"),
            "tutor_model": cfg.get("tutor_model", "?"),
            "started_at": cfg.get("started_at", ""),
            "mean_normalized": summary.get("mean_normalized") if summary else None,
            "problems": problems,
            "_mtime": tag_dir.stat().st_mtime,
        })

    def sort_key(r: dict[str, Any]) -> tuple[int, float, str]:
        if r["tag"] in PINNED_TAGS:
            return (0, PINNED_TAGS.index(r["tag"]), "")
        return (1, r["_mtime"], r["tag"])

    return sorted(out, key=sort_key)


def _load_difficulties() -> dict[str, str]:
    if not PROBLEMS_PATH.exists():
        return {}
    try:
        problems = json.loads(PROBLEMS_PATH.read_text())
        return {p["slug"]: p.get("difficulty", "") for p in problems}
    except Exception:
        return {}


def _row_mean(slug: str, runs: list[dict[str, Any]]) -> float | None:
    scores = []
    for r in runs:
        p = next((p for p in r["problems"] if p["slug"] == slug), None)
        if p and p.get("normalized") is not None:
            scores.append(p["normalized"])
    return sum(scores) / len(scores) if scores else None


def _all_slugs(runs: list[dict[str, Any]]) -> list[str]:
    """Union of all problem slugs across runs, in the order they first appear."""
    seen: dict[str, None] = {}
    for r in runs:
        for p in r["problems"]:
            seen.setdefault(p["slug"], None)
    return list(seen.keys())


def _render_matrix(
    runs: list[dict[str, Any]],
    slugs: list[str],
    difficulties: dict[str, str],
) -> str:
    """The heatmap: rows = slugs, cols = runs. Each cell's bg is the
    normalized score color. Clickable to load the matching transcript.
    Each row carries data-difficulty and data-mean for client-side
    filter/sort."""
    rows = []

    # Mean row at the top — never filtered/sorted.
    mean_cells = []
    for r in runs:
        m = r.get("mean_normalized")
        bg = _score_color(m)
        fg = _score_text_color(m)
        text = f"{m:.2f}" if m is not None else "—"
        mean_cells.append(
            f'<td class="mean-cell" style="background:{bg};color:{fg};">{text}</td>'
        )
    rows.append(
        '<tr class="mean-row">'
        '<td class="slug-cell mean-label">MEAN</td>'
        + "".join(mean_cells) +
        '</tr>'
    )

    # One row per problem.
    for order_idx, slug in enumerate(slugs):
        cells = []
        for r in runs:
            problem = next((p for p in r["problems"] if p["slug"] == slug), None)
            if problem is None or not problem["jsonl"].exists():
                cells.append('<td class="cell empty">—</td>')
                continue
            score = problem["normalized"]
            bg = _score_color(score)
            fg = _score_text_color(score)
            text = f"{score:.2f}" if score is not None else "?"
            cells.append(
                f'<td class="cell" data-tag="{html.escape(r["tag"])}" data-slug="{html.escape(slug)}" '
                f'style="background:{bg};color:{fg};">{text}</td>'
            )
        difficulty = difficulties.get(slug, "")
        mean = _row_mean(slug, runs)
        mean_attr = f' data-mean="{mean:.4f}"' if mean is not None else ""
        rows.append(
            f'<tr data-slug="{html.escape(slug)}" data-difficulty="{html.escape(difficulty)}" '
            f'data-order="{order_idx}"{mean_attr}>'
            f'<td class="slug-cell">{html.escape(slug)}</td>{"".join(cells)}</tr>'
        )

    headers = "".join(
        f'<th class="run-header" data-tag="{html.escape(r["tag"])}" title="click to sort">'
        f'<div class="run-tag">{html.escape(r["tag"])} <span class="sort-arrow"></span></div>'
        f'</th>'
        for r in runs
    )
    return (
        '<table class="matrix"><thead>'
        f'<tr><th class="slug-header">problem</th>{headers}</tr>'
        '</thead>'
        f'<tbody>{"".join(rows)}</tbody>'
        '</table>'
    )


def _render_controls() -> str:
    return (
        '<div class="controls">'
        '<div class="control-group">'
        '<span class="control-label">Difficulty</span>'
        '<button class="ctl active" data-filter="all">all</button>'
        '<button class="ctl" data-filter="easy">easy</button>'
        '<button class="ctl" data-filter="medium">medium</button>'
        '<button class="ctl" data-filter="hard">hard</button>'
        '</div>'
        '</div>'
    )


def _render_transcript_panels(runs: list[dict[str, Any]]) -> str:
    """One hidden <div> per (tag, slug). JS unhides the selected one."""
    parts = []
    for r in runs:
        for p in r["problems"]:
            tag = r["tag"]
            slug = p["slug"]
            try:
                body = render_transcript_body(p["jsonl"])
            except Exception as e:
                body = f'<div class="error">Failed to render: {html.escape(str(e))}</div>'
            parts.append(
                f'<div class="panel" data-tag="{html.escape(tag)}" data-slug="{html.escape(slug)}" hidden>'
                f'{body}'
                f'</div>'
            )
    return "".join(parts)


# ============================================================================
# CSS / JS
# ============================================================================

TRANSCRIPT_CSS = """
:root { color-scheme: dark; }
* { box-sizing: border-box; }
body {
  font: 13.5px/1.55 -apple-system, "Segoe UI", Helvetica, sans-serif;
  background: #1a1a1a; color: #e0e0e0;
}
.mono { font-family: "SF Mono", "Cascadia Code", Menlo, Consolas, monospace; }
h1 { color: #fff; margin: 0 0 4px 0; font-size: 22px; }
h2 { color: #c0c5cc; margin: 24px 0 8px 0; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; }
.meta { color: #949494; font-size: 12px; margin-bottom: 14px; }
.problem-prompt { background: #111; border-left: 3px solid #5c6370; padding: 10px 14px; margin: 12px 0 24px 0; color: #c0c5cc; }
.turn { margin-top: 28px; padding-top: 18px; border-top: 1px solid #2a2a2a; }
.turn-header { color: #6f6f6f; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 12px; }

.assistant, .user { display: flex; margin-top: 14px; gap: 8px; }
.marker { width: 14px; flex-shrink: 0; line-height: 1.55; font-size: 14px; color: #c0c5cc; }
.user-marker { color: #c0c5cc; }
.assistant-body, .user-body { flex: 1; min-width: 0; }
.assistant-body p, .user-body p { margin: 0 0 8px 0; }
.assistant-body p:last-child, .user-body p:last-child { margin-bottom: 0; }

p code { background: #2a2a2a; padding: 1px 5px; border-radius: 3px; font-family: "SF Mono", Menlo, monospace; font-size: 12.5px; color: #f0f0f0; }
pre { background: #0d0d0d; padding: 10px 12px; border-radius: 4px; overflow-x: auto; margin: 8px 0; font-family: "SF Mono", Menlo, monospace; font-size: 12px; line-height: 1.5; }
pre code { background: none; padding: 0; font-family: inherit; font-size: inherit; }

.thinking { color: #696969; margin: 10px 0 4px 22px; }
.thinking summary { cursor: pointer; font-style: italic; font-size: 12.5px; color: #6f6f6f; }
.thinking-body { padding: 8px 0 8px 12px; border-left: 1px dashed #3a3a3a; font-style: italic; white-space: pre-wrap; color: #888; margin-top: 6px; font-size: 12.5px; }

.tool { margin: 12px 0 12px 0; }
.tool-head { font-family: "SF Mono", Menlo, monospace; font-size: 13px; }
.dot { font-size: 14px; }
.dot-done { color: #50c850; }
.dot-error { color: #ff8787; }
.tool-name { font-weight: 700; color: #f0f0f0; }
.tool-cont { color: #949494; padding-left: 18px; font-family: "SF Mono", Menlo, monospace; font-size: 12.5px; margin-top: 2px; }
.tool-cont.err { color: #ff8787; }

/* Diff coloring matches Diff.tsx (ADD_FG/DEL_FG/HUNK_FG/META_FG) */
pre.diff { padding: 6px 0; line-height: 1.4; }
.diff-add, .diff-del, .diff-ctx, .diff-meta, .diff-hunk {
  display: block; padding: 0 12px; white-space: pre-wrap; word-break: break-all;
  font-family: "SF Mono", Menlo, monospace; font-size: 12px;
}
.diff-add { background: #022800; color: #50c850; }
.diff-del { background: #3d0100; color: #dc5a5a; }
.diff-ctx { color: #f8f8f2; }
.diff-hunk { color: #66d9ef; background: rgba(102, 217, 239, 0.06); }
.diff-meta { color: #999999; }
.diff-num { color: #696969; display: inline-block; width: 32px; text-align: right; user-select: none; }

.options { display: flex; gap: 12px; margin: 14px 0 8px 22px; align-items: stretch; }
.opt { flex: 1; min-width: 0; border: 1px solid #5c6370; border-radius: 8px; padding: 10px 14px; background: #1a1a1a; overflow: hidden; }
.opt-title { font-weight: 700; color: #e0e0e0; margin-bottom: 6px; font-size: 13.5px; }
.opt-body { font-size: 13px; }
.opt-body p { margin: 0 0 6px 0; }
.opt-body pre { margin: 6px 0; }
.opt-best { border-color: #50c850; }
.opt-best .opt-title::after { content: " ★"; color: #50c850; font-size: 11px; vertical-align: super; }

.private { margin: 0 0 12px 22px; padding: 6px 12px; font-size: 12px; color: #696969; }
.private summary { cursor: pointer; }
.private-body { padding-top: 6px; color: #999; white-space: pre-wrap; }

.leak { background: #3d0100; border: 1px solid #ff8787; padding: 8px 12px; border-radius: 4px; margin: 10px 0; color: #ff8787; font-size: 13px; }

.grade { margin: 18px 0 24px 0; background: #131313; border: 1px solid #2a2a2a; border-radius: 6px; padding: 0; overflow: hidden; }
.grade > summary { padding: 10px 14px; cursor: pointer; color: #c0c5cc; font-size: 13px; background: #181818; user-select: none; }
.grade > summary:hover { background: #1f1f1f; }
.grade-table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
.grade-table tr.grade-cat td { color: #6f6f6f; font-size: 10.5px; letter-spacing: 1.2px; padding: 10px 14px 4px 14px; border-top: 1px solid #2a2a2a; }
.grade-table tr.grade-cat:first-child td { border-top: none; }
.grade-table tr.grade-row td { padding: 5px 14px; vertical-align: top; }
.grade-name { color: #c0c5cc; width: 160px; font-family: "SF Mono", Menlo, monospace; font-size: 12px; }
.grade-score { width: 40px; text-align: center; }
.grade-rationale { color: #999; padding-right: 14px !important; }
.score-badge { display: inline-block; min-width: 22px; padding: 2px 6px; border-radius: 4px; font-weight: 700; font-family: "SF Mono", Menlo, monospace; font-size: 11.5px; }
.score-hi { background: #022800; color: #50c850; }
.score-mid { background: #2a2410; color: #e6db74; }
.score-lo { background: #3d0100; color: #dc5a5a; }
"""


VIEWER_CSS = """
/* Override transcript body styling so the SPA layout fills the viewport. */
body { margin: 0; padding: 0; background: #0d0d0d; }
/* Sidebar takes whatever the matrix needs (no horizontal scroll); detail
   gets the rest. min-width: 0 on .detail is the standard fix for grid
   children that contain wide content (otherwise they push out the layout). */
.layout { display: grid; grid-template-columns: max-content 1fr; height: 100vh; }
.sidebar { background: #131313; border-right: 1px solid #2a2a2a; overflow-y: auto; overflow-x: hidden; padding: 14px 12px; min-width: 0; }
.detail { overflow: auto; padding: 24px 32px; min-width: 0; }

.app-header { padding: 4px 4px 12px 4px; border-bottom: 1px solid #2a2a2a; margin-bottom: 12px; }
.app-title { font-size: 16px; font-weight: 700; color: #fff; margin: 0; }
.app-meta { font-size: 11.5px; color: #696969; margin-top: 4px; font-family: "SF Mono", Menlo, monospace; }

.matrix { border-collapse: collapse; font-size: 11px; width: 100%; }
.matrix th, .matrix td { padding: 4px 6px; text-align: center; border: 1px solid #1a1a1a; }
.matrix .slug-header { text-align: left; color: #6f6f6f; font-weight: 400; padding-left: 8px; }
.matrix .run-header { color: #c0c5cc; font-weight: 600; cursor: pointer; user-select: none; }
.matrix .run-header:hover { background: #1a1a1a; }
.matrix .run-header.sorted { color: #66d9ef; }
.matrix .run-tag { font-size: 11.5px; }
.matrix .sort-arrow { font-size: 10px; color: #66d9ef; }
.matrix .slug-cell { text-align: left; color: #c0c5cc; font-family: "SF Mono", Menlo, monospace;
                     font-size: 11px; padding-left: 8px; padding-right: 10px; white-space: nowrap; }
.matrix .cell, .matrix .mean-cell { font-family: "SF Mono", Menlo, monospace; font-weight: 700;
                                     font-size: 11px; cursor: pointer; min-width: 38px; }
.matrix .cell:hover { outline: 1px solid #66d9ef; outline-offset: -1px; position: relative; z-index: 1; }
.matrix .cell.selected { outline: 2px solid #66d9ef; outline-offset: -2px; position: relative; z-index: 1; }
.matrix .cell.empty { color: #444; cursor: default; }
.matrix .mean-row td { border-bottom: 2px solid #444; font-size: 11.5px; }
.matrix .mean-row .mean-label { color: #6f6f6f; font-weight: 700; letter-spacing: 1px; font-size: 10.5px; }

.placeholder { color: #696969; font-style: italic; padding: 60px 20px; text-align: center; }
.detail h1 { margin-top: 0; }

.error { color: #ff8787; padding: 20px; }

.controls { display: flex; flex-direction: column; gap: 8px; margin: 10px 0 14px 0; padding: 8px 4px; border-bottom: 1px solid #2a2a2a; }
.control-group { display: flex; align-items: center; gap: 6px; }
.control-label { color: #696969; font-size: 10.5px; letter-spacing: 1.2px; text-transform: uppercase; min-width: 38px; }
.ctl { background: #1a1a1a; border: 1px solid #2a2a2a; color: #c0c5cc; padding: 3px 8px;
       font: 11px "SF Mono", Menlo, monospace; border-radius: 3px; cursor: pointer; }
.ctl:hover { border-color: #5c6370; color: #e0e0e0; }
.ctl.active { background: #2a2a2a; border-color: #66d9ef; color: #66d9ef; }
"""


VIEWER_JS = """
(function() {
  const panels = document.querySelectorAll('.panel');
  const cells = document.querySelectorAll('.cell[data-tag]');
  const detail = document.getElementById('detail');
  const placeholder = document.getElementById('placeholder');
  const tbody = document.querySelector('table.matrix tbody');
  const rows = Array.from(tbody.querySelectorAll('tr[data-slug]'));
  const meanRow = tbody.querySelector('tr.mean-row');

  let currentFilter = 'all';
  // Sort state: which column tag (or null for default order) and direction.
  // Cycle on each column header click: null → desc → asc → null.
  let sortTag = null;
  let sortDir = null;

  function show(tag, slug) {
    panels.forEach(p => { p.hidden = true; });
    cells.forEach(c => c.classList.remove('selected'));
    const target = document.querySelector(`.panel[data-tag="${CSS.escape(tag)}"][data-slug="${CSS.escape(slug)}"]`);
    const cell   = document.querySelector(`.cell[data-tag="${CSS.escape(tag)}"][data-slug="${CSS.escape(slug)}"]`);
    if (target) {
      target.hidden = false;
      placeholder.hidden = true;
      detail.scrollTop = 0;
    }
    if (cell) cell.classList.add('selected');
    history.replaceState(null, '', `#${encodeURIComponent(tag)}/${encodeURIComponent(slug)}`);
  }

  function cellScore(row, tag) {
    const c = row.querySelector(`.cell[data-tag="${CSS.escape(tag)}"]`);
    if (!c) return NaN;
    const v = parseFloat(c.textContent);
    return Number.isFinite(v) ? v : NaN;
  }

  function updateHeaderArrows() {
    document.querySelectorAll('.run-header').forEach(h => {
      const arrow = h.querySelector('.sort-arrow');
      if (h.dataset.tag === sortTag && sortDir) {
        arrow.textContent = sortDir === 'desc' ? '↓' : '↑';
        h.classList.add('sorted');
      } else {
        arrow.textContent = '';
        h.classList.remove('sorted');
      }
    });
  }

  function applyFilterSort() {
    // Filter: hide rows whose data-difficulty doesn't match.
    rows.forEach(r => {
      r.hidden = currentFilter !== 'all' && r.dataset.difficulty !== currentFilter;
    });
    // Sort: by selected column's score, or restore default order if no
    // active sort. Missing scores sink to the bottom either direction.
    let sorted;
    if (!sortTag || !sortDir) {
      sorted = [...rows].sort((a, b) =>
        parseInt(a.dataset.order) - parseInt(b.dataset.order)
      );
    } else {
      sorted = [...rows].sort((a, b) => {
        const ma = cellScore(a, sortTag);
        const mb = cellScore(b, sortTag);
        const aMissing = Number.isNaN(ma);
        const bMissing = Number.isNaN(mb);
        if (aMissing && bMissing) return 0;
        if (aMissing) return 1;
        if (bMissing) return -1;
        return sortDir === 'asc' ? ma - mb : mb - ma;
      });
    }
    sorted.forEach(r => tbody.appendChild(r));
    if (meanRow) tbody.insertBefore(meanRow, tbody.firstChild);
  }

  function cycleSort(tag) {
    if (sortTag !== tag) {
      sortTag = tag;
      sortDir = 'desc';
    } else if (sortDir === 'desc') {
      sortDir = 'asc';
    } else {
      sortTag = null;
      sortDir = null;
    }
    updateHeaderArrows();
    applyFilterSort();
  }

  cells.forEach(cell => {
    cell.addEventListener('click', () => show(cell.dataset.tag, cell.dataset.slug));
  });

  document.querySelectorAll('.run-header[data-tag]').forEach(h => {
    h.addEventListener('click', () => cycleSort(h.dataset.tag));
  });

  document.querySelectorAll('button[data-filter]').forEach(b => {
    b.addEventListener('click', () => {
      document.querySelectorAll('button[data-filter]').forEach(x => x.classList.remove('active'));
      b.classList.add('active');
      currentFilter = b.dataset.filter;
      applyFilterSort();
    });
  });

  // Open from hash on load (e.g. #refined-3/leetcode-two-sum). Otherwise
  // leave the placeholder visible — no auto-select of the first transcript.
  const hash = decodeURIComponent(window.location.hash.slice(1));
  if (hash.includes('/')) {
    const [tag, slug] = hash.split('/', 2);
    show(tag, slug);
  }
})();
"""


# ============================================================================
# top-level assembly + CLI
# ============================================================================

def render_viewer(runs_dir: Path) -> str:
    runs = _discover_runs(runs_dir)
    if not runs:
        return "<!doctype html><html><body><h1>No runs found.</h1></body></html>"
    difficulties = _load_difficulties()
    slugs = _all_slugs(runs)

    matrix_html = _render_matrix(runs, slugs, difficulties)
    controls_html = _render_controls()
    panels_html = _render_transcript_panels(runs)
    n_runs = len(runs)
    n_problems = len(slugs)
    generated = time.strftime("%Y-%m-%d %H:%M:%S")

    sidebar = (
        '<div class="app-header">'
        '<h1 class="app-title">Pairing mode eval viewer</h1>'
        f'<div class="app-meta">{n_runs} runs · {n_problems} problems · generated {generated}</div>'
        '</div>'
        + controls_html
        + matrix_html
    )

    return (
        '<!doctype html><html><head><meta charset="utf-8">'
        '<title>Pairing mode eval viewer</title>'
        f'<style>{TRANSCRIPT_CSS}\n{VIEWER_CSS}</style>'
        '</head><body>'
        '<div class="layout">'
        f'<aside class="sidebar">{sidebar}</aside>'
        f'<main class="detail" id="detail">'
        '<div class="placeholder" id="placeholder">click a cell on the left to load a transcript</div>'
        f'{panels_html}'
        '</main>'
        '</div>'
        f'<script>{VIEWER_JS}</script>'
        '</body></html>'
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("-o", "--output", default=str(REPO_ROOT / "eval_viewer.html"))
    p.add_argument("--runs-dir", default=str(RUNS_DIR))
    args = p.parse_args(argv if argv is not None else sys.argv[1:])

    runs_dir = Path(args.runs_dir)
    out_path = Path(args.output)
    html_str = render_viewer(runs_dir)
    out_path.write_text(html_str)
    size_mb = out_path.stat().st_size / 1024 / 1024
    print(f"wrote {out_path}  ({size_mb:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
