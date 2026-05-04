"""Eval runner: one tutor condition × N problems → one tagged run directory.

  uv run --env-file .env run.py --condition regular --tag initial -n 36

Layout produced:
  eval/runs/<tag>/
    config.json
    summary.json
    <problem-slug>/
      transcript.md
      transcript.jsonl
      result.json
      files/         # whatever the tutor wrote in its sandbox
"""

import argparse
import asyncio
import dataclasses
import json
import re
import shutil
import sys
import tempfile
import time
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from anthropic import AsyncAnthropic
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
    ThinkingBlock,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
    create_sdk_mcp_server,
)

from propose_options import propose_options as propose_options_tool


SCHEMA_PATH = Path(__file__).parent.parent / "propose_options_tool_schema.json"
SCHEMA = json.loads(SCHEMA_PATH.read_text())
MCP_SERVER_NAME = SCHEMA["mcp_server_name"]
TOOL_NAME = SCHEMA["tool_name"]
FULL_PROPOSE_TOOL_NAME = f"mcp__{MCP_SERVER_NAME}__{TOOL_NAME}"

MAX_TOOL_OUTPUT_LINES = 12


def _truncate_lines(text: str, max_lines: int) -> str:
    lines = text.split("\n")
    if len(lines) <= max_lines:
        return text
    return "\n".join(lines[:max_lines]) + f"\n… ({len(lines) - max_lines} more lines)"


def _summarize_input(name: str, args: dict[str, Any]) -> str:
    if name == "Bash":
        return str(args.get("command", ""))
    if name in ("Read", "Edit", "Write"):
        return str(args.get("file_path", ""))
    if name in ("Glob", "Grep"):
        return str(args.get("pattern", ""))
    try:
        s = json.dumps(args)
        return s if len(s) <= 80 else s[:77] + "..."
    except Exception:
        return ""


def _render_tool_use(block: ToolUseBlock) -> str:
    arg = _summarize_input(block.name, block.input)
    head = f"[{block.name}({arg})]" if arg else f"[{block.name}]"
    if block.name == "Edit":
        old = str(block.input.get("old_string", ""))
        new = str(block.input.get("new_string", ""))
        return f"{head}\n--- before\n{old}\n--- after\n{new}"
    if block.name == "Write":
        content = str(block.input.get("content", ""))
        return f"{head}\n{_truncate_lines(content, MAX_TOOL_OUTPUT_LINES)}"
    return head


def _render_tool_result(block: ToolResultBlock) -> str:
    if isinstance(block.content, str):
        text = block.content
    elif isinstance(block.content, list):
        text = "".join(c.get("text", "") for c in block.content if isinstance(c, dict))
    else:
        text = ""
    text = text.strip()
    if block.is_error:
        return f"  error: {text.splitlines()[0] if text else ''}"
    if not text:
        return "  (no output)"
    indented = "\n".join("  " + line for line in _truncate_lines(text, MAX_TOOL_OUTPUT_LINES).split("\n"))
    return indented


def _render_propose_options(block: ToolUseBlock, for_user: bool) -> str:
    a = block.input
    a_title = a.get("option_a_title", "")
    a_body = a.get("option_a_body", "").strip()
    b_title = a.get("option_b_title", "")
    b_body = a.get("option_b_body", "").strip()
    lines = [
        "OPTIONS:",
        f"[A] {a_title}",
        a_body,
        "",
        f"[B] {b_title}",
        b_body,
        "",
        "(Reply with A or B, or ask a follow-up question.)",
    ]
    if not for_user:
        # Human transcript: include the tutor's private notes for review.
        best = a.get("best_letter", "")
        rationale = a.get("rationale", "").strip()
        lines.extend([
            "",
            f"PRIVATE: best={best}",
            f"PRIVATE: rationale={rationale}",
        ])
    return "\n".join(lines)


def render_turn(messages: list[Any], for_user: bool = False) -> str:
    """Render a tutor turn's SDK messages as a clean text block.

    `for_user=True` strips everything the student must not see:
    - ThinkingBlocks (often state the tutor's preferred option directly)
    - The propose_options tool's `best_letter` and `rationale` private fields

    `for_user=False` shows everything for human review.

    The propose_options tool result ("Options recorded; awaiting user
    selection.") is always suppressed since the rendered OPTIONS block
    replaces it.
    """
    lines: list[str] = []
    suppressed_tool_ids: set[str] = set()

    for msg in messages:
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, TextBlock):
                    if block.text.strip():
                        lines.append("Tutor: " + block.text.strip())
                        lines.append("")
                elif isinstance(block, ThinkingBlock):
                    if not for_user and block.thinking.strip():
                        thinking_indented = block.thinking.strip().replace("\n", "\n  ")
                        lines.append("Thinking: " + thinking_indented)
                        lines.append("")
                elif isinstance(block, ToolUseBlock):
                    if block.name == FULL_PROPOSE_TOOL_NAME:
                        lines.append(_render_propose_options(block, for_user=for_user))
                        lines.append("")
                        suppressed_tool_ids.add(block.id)
                    else:
                        lines.append(_render_tool_use(block))
        elif isinstance(msg, UserMessage):
            content = msg.content if isinstance(msg.content, list) else []
            for block in content:
                if isinstance(block, ToolResultBlock):
                    if block.tool_use_id in suppressed_tool_ids:
                        continue
                    lines.append(_render_tool_result(block))
                    lines.append("")
        elif isinstance(msg, ResultMessage):
            pass

    return "\n".join(lines).strip()


# ---------- tutor configuration ----------

Condition = Literal["baseline", "learning", "regular"]

# Shared with tui/src/pair/systemPrompt.ts via the same file at the repo
# root, the same way the propose_options schema is shared.
PROMPT_PATH = Path(__file__).parent.parent / "pairing_prompt.md"
PAIR_SYSTEM_PROMPT = PROMPT_PATH.read_text().strip()


TUTOR_FILE_TOOLS = ["Read", "Glob", "Grep", "Edit", "Write", "Bash"]
# AskUserQuestion is auto-exposed by the SDK and would let the model bypass
# propose_options for didactic moments. Disallow it across all conditions
# for symmetry (baseline shouldn't have it either, since the prior eval
# never gave it any condition).
TUTOR_DISALLOWED = ["AskUserQuestion"]


def setup_sandbox(condition: Condition, parent: Path | None = None) -> Path:
    """Create a per-run /tmp sandbox cwd. For 'learning' condition, drops a
    .claude/settings.json with outputStyle so settingSources=['project']
    actually picks it up (per-query outputStyle alone is silently ignored
    by the SDK — confirmed in the prior TS eval's diag-init.ts)."""
    sandbox = Path(tempfile.mkdtemp(prefix="ai-pair-eval-", dir=parent))
    if condition == "learning":
        claude_dir = sandbox / ".claude"
        claude_dir.mkdir()
        (claude_dir / "settings.json").write_text(
            json.dumps({"outputStyle": "Learning"})
        )
    return sandbox


def make_tutor_options(
    condition: Condition,
    sandbox_dir: Path,
    model: str = "claude-sonnet-4-6",
) -> ClaudeAgentOptions:
    """Build the SDK options for the tutor side under a given condition.

    - baseline: no system prompt, no propose_options, basic file tools.
    - learning: same as baseline + Learning output style (requires the
      sandbox to have .claude/settings.json — call setup_sandbox first).
    - regular:  pair system prompt + propose_options MCP server registered.
    """
    common = dict(
        model=model,
        permission_mode="bypassPermissions",
        cwd=str(sandbox_dir),
        disallowed_tools=TUTOR_DISALLOWED,
    )

    if condition == "baseline":
        return ClaudeAgentOptions(
            system_prompt="",
            allowed_tools=TUTOR_FILE_TOOLS,
            **common,
        )

    if condition == "learning":
        return ClaudeAgentOptions(
            system_prompt="",
            allowed_tools=TUTOR_FILE_TOOLS,
            setting_sources=["project"],
            **common,
        )

    # regular
    server = create_sdk_mcp_server(
        name=MCP_SERVER_NAME,
        version="0.1.0",
        tools=[propose_options_tool],
    )
    return ClaudeAgentOptions(
        system_prompt=PAIR_SYSTEM_PROMPT,
        allowed_tools=TUTOR_FILE_TOOLS + [FULL_PROPOSE_TOOL_NAME],
        mcp_servers={MCP_SERVER_NAME: server},
        **common,
    )


# Note: ClaudeSDKClient.get_mcp_status() only reports CLI-side MCP servers
# (the claude.ai integrations); in-process SDK MCP servers — which is what
# we use — are invisible to it. Confirmed via diag_mcp_status.py. So we
# can't proactively verify propose_options is registered. Instead, the
# runner counts propose_options invocations after the run; zero in a regular
# condition is the symptom of a registration failure.


# ---------- student side ----------

STUDENT_SYSTEM_PROMPT = """
You are a junior software engineer working through a small coding problem with an AI pair-programming partner. You would like to solve the problem but also learn along the way.

You are the USER role in this conversation; the pair is the assistant. Write only your own next reply — never write the pair's response, never narrate in the second person ("you should…"), never use the pair's voice ("I'll walk you through it…"). Stay in your own voice as the junior engineer asking and learning.

Stay focused on the original problem stated at the start of the session. If the pair offers to extend, generalize, or move on to a different problem, politely decline and wrap up — your goal is to solve the one problem you were given, not to start new work.

When the problem feels solved (the code works and there's nothing meaningful left to do), end your reply with the literal token <done/> on its own line. Don't emit <done/> prematurely — only when you'd actually wrap up the session.
""".strip()


_DONE_RE = re.compile(r"(^|\n)\s*<done\s*/?>\s*(\n|$)")


def is_done(reply: str) -> bool:
    """True if the student's reply contains a `<done/>` sentinel line."""
    return bool(_DONE_RE.search(reply))


def strip_done(reply: str) -> str:
    """Remove the `<done/>` sentinel for the version sent back to the tutor."""
    return _DONE_RE.sub(lambda m: m.group(1), reply).strip()


@dataclass
class Student:
    """Simulated junior engineer. Raw Anthropic API, history managed here.

    The student is the test harness, not the system under test, so we
    intentionally give it no agent harness — just text in, text out, with
    a manually-tracked messages list. This sidesteps thinking-block leaks
    and SDK init-handshake races that would happen if both sides used the
    agent SDK.
    """

    problem_prompt: str
    model: str = "claude-haiku-4-5-20251001"
    max_tokens: int = 1024
    system_prompt: str = STUDENT_SYSTEM_PROMPT
    history: list[dict[str, str]] = field(default_factory=list)
    _client: AsyncAnthropic | None = None

    def __post_init__(self) -> None:
        self._client = AsyncAnthropic()

    async def reply(self, tutor_rendered: str) -> str:
        """Send the latest tutor turn (rendered with for_user=True) and
        return the student's plain-text reply. On the first turn the
        problem prompt is prepended so the student knows what they're
        working on."""
        if not self.history:
            user_content = (
                f"(You're working on this problem with the pair: "
                f"{self.problem_prompt})\n\n---\n\n{tutor_rendered}"
            )
        else:
            user_content = tutor_rendered

        self.history.append({"role": "user", "content": user_content})
        assert self._client is not None
        response = await self._client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system_prompt,
            messages=self.history,  # type: ignore[arg-type]
        )
        text = "".join(
            block.text for block in response.content if block.type == "text"
        ).strip()
        self.history.append({"role": "assistant", "content": text})
        return text


# ---------- orchestration ----------

DEFAULT_TUTOR_MODEL = "claude-sonnet-4-6"
DEFAULT_STUDENT_MODEL = "claude-haiku-4-5-20251001"
DEFAULT_MAX_TURNS = 50
# Reject a turn if no events arrive for this long. Prevents silent hangs
# if the SDK subprocess dies or the OS suspends the process.
TURN_IDLE_TIMEOUT_S = 10 * 60


def _serialize(obj: Any) -> Any:
    """Make SDK dataclasses JSON-serializable for the raw transcript."""
    if dataclasses.is_dataclass(obj):
        return {"__type__": type(obj).__name__, **dataclasses.asdict(obj)}
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_serialize(x) for x in obj]
    return obj


class JsonlWriter:
    """Append-only JSONL writer with `kind` discriminator."""

    def __init__(self, path: Path) -> None:
        self._fp = path.open("w")

    def write(self, kind: str, **fields: Any) -> None:
        rec = {"kind": kind, "ts": time.time(), **{k: _serialize(v) for k, v in fields.items()}}
        self._fp.write(json.dumps(rec) + "\n")
        self._fp.flush()

    def close(self) -> None:
        self._fp.close()


async def _collect_tutor_turn(client: ClaudeSDKClient) -> list[Any]:
    """Drain the tutor's response stream until ResultMessage. Bounded by
    TURN_IDLE_TIMEOUT_S to surface SDK hangs instead of blocking forever."""
    messages: list[Any] = []

    async def _drain() -> None:
        async for msg in client.receive_response():
            messages.append(msg)
            if isinstance(msg, ResultMessage):
                return

    await asyncio.wait_for(_drain(), timeout=TURN_IDLE_TIMEOUT_S)
    return messages


def _harvest_sandbox(sandbox: Path, dest: Path) -> None:
    """Copy the tutor's working directory into the run dir for review.
    Skips Python bytecode and the .claude/ settings dir we may have planted."""

    def ignore(_: str, names: list[str]) -> list[str]:
        return [n for n in names if n in ("__pycache__", ".claude") or n.endswith(".pyc")]

    dest.mkdir(parents=True, exist_ok=True)
    for child in sandbox.iterdir():
        if child.name in ("__pycache__", ".claude") or child.name.endswith(".pyc"):
            continue
        target = dest / child.name
        if child.is_dir():
            shutil.copytree(child, target, ignore=ignore)
        else:
            shutil.copy2(child, target)


def _audit_no_leak(student_view: str, messages: list[Any]) -> list[str]:
    """Scan what the student saw for substrings the student must not see —
    the tutor's thinking, the propose_options rationale, and best_letter
    markers. Returns a list of leak descriptions (empty if clean)."""
    leaks: list[str] = []
    for msg in messages:
        if not isinstance(msg, AssistantMessage):
            continue
        for block in msg.content:
            if isinstance(block, ThinkingBlock):
                snippet = block.thinking.strip()[:60]
                if snippet and snippet in student_view:
                    leaks.append(f"thinking-block snippet leaked: {snippet!r}")
            elif isinstance(block, ToolUseBlock) and block.name == FULL_PROPOSE_TOOL_NAME:
                rationale = str(block.input.get("rationale", "")).strip()
                if rationale and rationale[:60] in student_view:
                    leaks.append(f"propose_options rationale leaked: {rationale[:60]!r}")
                if "best_letter" in student_view or "best=A" in student_view or "best=B" in student_view:
                    leaks.append("best_letter marker present in student view")
    return leaks


@dataclass
class RunResult:
    slug: str
    condition: str
    end_reason: Literal["done", "max_turns", "error", "mcp_failed"]
    turns: int
    duration_s: float
    propose_options_calls: int
    leaks_detected: int
    error: str | None = None


async def run_one(
    problem: dict[str, Any],
    condition: Condition,
    out_dir: Path,
    tutor_model: str = DEFAULT_TUTOR_MODEL,
    student_model: str = DEFAULT_STUDENT_MODEL,
    max_turns: int = DEFAULT_MAX_TURNS,
) -> RunResult:
    """Run one (problem, condition) cell.

    Writes:
      - transcript.jsonl: raw SDK messages + render + leakage audit
      - transcript.md: human view (includes Thinking blocks + PRIVATE
        notes from propose_options, useful for review)
      - transcript_grader.md: same conversation but with the tutor's turns
        rendered the way the student saw them (no thinking, no PRIVATE)
        — this is what the grader reads, so the grader judges only the
        observable interaction, not the model's preferred answer
      - result.json: summary
      - files/: whatever the tutor wrote in its sandbox

    Returns a RunResult for aggregate summary.
    """
    slug = problem["slug"]
    run_dir = out_dir / slug
    run_dir.mkdir(parents=True, exist_ok=True)
    sandbox = setup_sandbox(condition)
    jsonl = JsonlWriter(run_dir / "transcript.jsonl")
    md = (run_dir / "transcript.md").open("w")
    grader_md = (run_dir / "transcript_grader.md").open("w")

    started_at = time.time()
    propose_calls = 0
    leak_count = 0
    end_reason: Literal["done", "max_turns", "error", "mcp_failed"] = "max_turns"
    error: str | None = None
    turn = 0

    try:
        opts = make_tutor_options(condition, sandbox, model=tutor_model)
        jsonl.write(
            "run_start",
            problem=problem,
            condition=condition,
            tutor_model=tutor_model,
            student_model=student_model,
            sandbox=str(sandbox),
            system_prompt=opts.system_prompt,
        )
        header = (
            f"# {slug}\n\n"
            f"- Condition: `{condition}`\n"
            f"- Tutor: `{tutor_model}` / Student: `{student_model}`\n"
            f"- Started: {time.strftime('%Y-%m-%dT%H:%M:%S')}\n\n"
            f"## Initial prompt\n\n{problem['prompt']}\n\n---\n\n"
        )
        md.write(header)
        grader_md.write(header)

        async with ClaudeSDKClient(options=opts) as tutor:
            student = Student(problem_prompt=problem["prompt"], model=student_model)
            next_for_tutor = problem["prompt"]

            while turn < max_turns:
                turn += 1
                jsonl.write("tutor_input", turn=turn, text=next_for_tutor)
                turn_header = f"## Turn {turn}\n\n### Tutor\n\n"
                md.write(turn_header)
                grader_md.write(turn_header)

                await tutor.query(next_for_tutor)
                tutor_messages = await _collect_tutor_turn(tutor)

                # Per-message raw record for post-hoc analysis.
                for m in tutor_messages:
                    jsonl.write("tutor_message", turn=turn, message=m)

                # Count propose_options invocations for this turn.
                for m in tutor_messages:
                    if isinstance(m, AssistantMessage):
                        for b in m.content:
                            if isinstance(b, ToolUseBlock) and b.name == FULL_PROPOSE_TOOL_NAME:
                                propose_calls += 1

                human_view = render_turn(tutor_messages, for_user=False)
                student_view = render_turn(tutor_messages, for_user=True)
                jsonl.write("tutor_render_human", turn=turn, text=human_view)
                jsonl.write("tutor_render_student", turn=turn, text=student_view)
                md.write(human_view + "\n\n")
                grader_md.write(student_view + "\n\n")

                # Runtime leakage audit on what the student is about to see.
                leaks = _audit_no_leak(student_view, tutor_messages)
                if leaks:
                    leak_count += len(leaks)
                    jsonl.write("leak_detected", turn=turn, leaks=leaks)
                    md.write(f"> **LEAK DETECTED:** {leaks}\n\n")

                student_reply = await student.reply(student_view)
                jsonl.write("student_reply", turn=turn, text=student_reply)
                student_section = f"### Student\n\n{student_reply.strip()}\n\n---\n\n"
                md.write(student_section)
                grader_md.write(student_section)

                if is_done(student_reply):
                    end_reason = "done"
                    break

                cleaned = strip_done(student_reply)
                if not cleaned:
                    end_reason = "done"  # empty reply = wrap up
                    break
                next_for_tutor = cleaned

    except asyncio.TimeoutError:
        end_reason = "error"
        error = f"turn idle for {TURN_IDLE_TIMEOUT_S}s — likely SDK hang"
    except Exception as e:
        end_reason = "error"
        error = f"{type(e).__name__}: {e}"
        traceback.print_exc()
    finally:
        duration_s = time.time() - started_at
        jsonl.write(
            "run_end", reason=end_reason, turns=turn,
            duration_s=duration_s, propose_options_calls=propose_calls,
            leaks_detected=leak_count, error=error,
        )
        footer = f"**Run end:** {end_reason} after {turn} turn(s) in {duration_s:.1f}s\n"
        if error:
            footer += f"\n**Error:** {error}\n"
        md.write(footer)
        grader_md.write(footer)
        md.close()
        grader_md.close()
        jsonl.close()
        _harvest_sandbox(sandbox, run_dir / "files")
        shutil.rmtree(sandbox, ignore_errors=True)

    result = RunResult(
        slug=slug, condition=condition, end_reason=end_reason,
        turns=turn, duration_s=duration_s,
        propose_options_calls=propose_calls, leaks_detected=leak_count,
        error=error,
    )
    (run_dir / "result.json").write_text(json.dumps(dataclasses.asdict(result), indent=2))
    return result


# ---------- CLI ----------

PROBLEMS_PATH = Path(__file__).parent / "problems.json"
RUNS_DIR = Path(__file__).parent / "runs"


def _timestamp() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def _load_problems(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text())


def _select_problems(
    all_problems: list[dict[str, Any]],
    n: int | None,
    ids: list[str] | None,
) -> list[dict[str, Any]]:
    if ids:
        by_slug = {p["slug"]: p for p in all_problems}
        missing = [s for s in ids if s not in by_slug]
        if missing:
            raise SystemExit(f"unknown problem slug(s): {missing}")
        return [by_slug[s] for s in ids]
    if n is not None:
        return all_problems[:n]
    return all_problems


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--condition", required=True, choices=["baseline", "learning", "regular"])
    p.add_argument("--tag", default=None, help="Run dir name under runs/. Default: timestamp.")
    p.add_argument("-n", "--num", type=int, default=None, help="Run only the first N problems.")
    p.add_argument("--problem-ids", default=None,
                   help="Comma-separated slugs to run (overrides -n).")
    p.add_argument("--max-turns", type=int, default=DEFAULT_MAX_TURNS)
    p.add_argument("--tutor-model", default=DEFAULT_TUTOR_MODEL)
    p.add_argument("--student-model", default=DEFAULT_STUDENT_MODEL)
    p.add_argument("--problems-file", default=str(PROBLEMS_PATH))
    p.add_argument("--runs-dir", default=str(RUNS_DIR))
    p.add_argument("-j", "--concurrency", type=int, default=1,
                   help="Run this many problems in parallel (asyncio gather + semaphore). "
                        "Each cell still gets its own ClaudeSDKClient + claude CLI subprocess "
                        "+ in-process MCP server, so they don't share state. Beware API rate "
                        "limits at high N.")
    p.add_argument("--dry-run", action="store_true", help="Print plan and exit.")
    return p.parse_args(argv)


async def _main_async(args: argparse.Namespace) -> int:
    all_problems = _load_problems(Path(args.problems_file))
    ids = [s.strip() for s in args.problem_ids.split(",")] if args.problem_ids else None
    problems = _select_problems(all_problems, args.num, ids)

    tag = args.tag or _timestamp()
    run_root = Path(args.runs_dir) / tag

    print(
        f"condition={args.condition}  tag={tag}  problems={len(problems)}  "
        f"tutor={args.tutor_model}  student={args.student_model}  max-turns={args.max_turns}"
    )
    print(f"out: {run_root}")
    for p in problems:
        print(f"  - {p['slug']}")

    if args.dry_run:
        return 0

    if run_root.exists() and any(run_root.iterdir()):
        print(f"refusing to overwrite non-empty run dir: {run_root}", file=sys.stderr)
        return 2

    run_root.mkdir(parents=True, exist_ok=True)
    (run_root / "config.json").write_text(json.dumps({
        "condition": args.condition,
        "tag": tag,
        "tutor_model": args.tutor_model,
        "student_model": args.student_model,
        "max_turns": args.max_turns,
        "problems": [p["slug"] for p in problems],
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }, indent=2))

    n_total = len(problems)
    semaphore = asyncio.Semaphore(max(1, args.concurrency))
    completed = 0

    async def run_with_progress(idx: int, problem: dict[str, Any]) -> RunResult:
        nonlocal completed
        async with semaphore:
            print(f"[{idx + 1}/{n_total}] ▶ {problem['slug']}")
            result = await run_one(
                problem=problem,
                condition=args.condition,
                out_dir=run_root,
                tutor_model=args.tutor_model,
                student_model=args.student_model,
                max_turns=args.max_turns,
            )
            completed += 1
            marker = "✓" if result.end_reason == "done" else "✗" if result.end_reason in ("error", "mcp_failed") else "·"
            line = (
                f"  {marker} [{completed}/{n_total}] {problem['slug']}: "
                f"{result.end_reason} after {result.turns} turns "
                f"({result.duration_s:.1f}s, propose_options×{result.propose_options_calls}, "
                f"leaks={result.leaks_detected})"
            )
            print(line)
            if result.error:
                print(f"    error: {result.error}")
            return result

    results = await asyncio.gather(
        *(run_with_progress(i, p) for i, p in enumerate(problems))
    )

    summary = {
        "tag": tag,
        "condition": args.condition,
        "n": len(results),
        "by_reason": {
            r: sum(1 for x in results if x.end_reason == r)
            for r in ("done", "max_turns", "error", "mcp_failed")
        },
        "total_propose_options_calls": sum(r.propose_options_calls for r in results),
        "total_leaks": sum(r.leaks_detected for r in results),
        "results": [dataclasses.asdict(r) for r in results],
    }
    (run_root / "summary.json").write_text(json.dumps(summary, indent=2))

    print(
        f"\nSummary: {summary['by_reason']}, "
        f"propose_options_calls={summary['total_propose_options_calls']}, "
        f"leaks={summary['total_leaks']}"
    )
    print(f"Run dir: {run_root}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv if argv is not None else sys.argv[1:])
    return asyncio.run(_main_async(args))


# ---------- self-test ----------

def _self_test() -> None:
    # Build a synthetic tutor turn: thinking → text → propose_options call →
    # tool_result (which should be suppressed). Verify both render modes.
    msgs = [
        AssistantMessage(
            content=[
                ThinkingBlock(
                    thinking="The user wants Game of Life. Best is the live-set approach (B), but I'll present both.",
                    signature="",
                ),
                TextBlock(text="Let's pick how to represent the grid."),
                ToolUseBlock(
                    id="tu_1",
                    name=FULL_PROPOSE_TOOL_NAME,
                    input={
                        "option_a_title": "2D array",
                        "option_a_body": "Fixed grid; iterate every cell each tick.",
                        "option_b_title": "Live set",
                        "option_b_body": "Store only live coordinates; implicitly infinite.",
                        "best_letter": "B",
                        "rationale": "Live set scales better for sparse boards.",
                    },
                ),
            ],
            model="claude-sonnet-4-6",
        ),
        UserMessage(
            content=[
                ToolResultBlock(
                    tool_use_id="tu_1",
                    content="Options recorded; awaiting user selection.",
                ),
            ],
        ),
        ResultMessage(
            subtype="success",
            duration_ms=1234,
            duration_api_ms=1000,
            is_error=False,
            num_turns=1,
            session_id="s",
            total_cost_usd=0.01,
        ),
    ]

    human = render_turn(msgs, for_user=False)
    student = render_turn(msgs, for_user=True)

    # Both views must include the options.
    for view, label in [(human, "human"), (student, "student")]:
        assert "[A] 2D array" in view, f"{label} view missing option A"
        assert "[B] Live set" in view, f"{label} view missing option B"
        assert "OPTIONS:" in view, f"{label} view missing OPTIONS header"
        assert "Tutor: Let's pick" in view, f"{label} view missing tutor text"
        # propose_options tool result must always be suppressed.
        assert "Options recorded" not in view, f"{label} leaked the suppressed tool result"

    # Human view must show thinking + private notes.
    assert "Thinking:" in human, "human view missing thinking block"
    assert "Live set scales better" in human, "human view missing rationale"
    assert "best=B" in human, "human view missing best_letter"

    # Student view must NOT show thinking, rationale, or best_letter.
    assert "Thinking:" not in student, "LEAK: student view contains thinking"
    assert "Live set scales better" not in student, "LEAK: student view contains rationale"
    assert "best=B" not in student, "LEAK: student view contains best_letter"
    assert "PRIVATE" not in student, "LEAK: student view contains PRIVATE marker"

    print("render_turn self-test: OK")


def _self_test_tutor_config() -> None:
    """Build options for each condition (no API calls). Verify shape only."""
    for cond in ("baseline", "learning", "regular"):
        sandbox = setup_sandbox(cond)  # type: ignore[arg-type]
        opts = make_tutor_options(cond, sandbox)  # type: ignore[arg-type]
        assert opts.cwd == str(sandbox), f"{cond}: cwd not set to sandbox"
        assert "AskUserQuestion" in (opts.disallowed_tools or []), f"{cond}: AskUserQuestion not disallowed"

        if cond == "baseline":
            assert opts.system_prompt == "", "baseline should have empty system prompt"
            assert not opts.mcp_servers, "baseline should have no MCP servers"
            assert FULL_PROPOSE_TOOL_NAME not in (opts.allowed_tools or []), "baseline should not allow propose_options"
            assert opts.setting_sources is None, "baseline should not set setting_sources"
            assert not (sandbox / ".claude").exists(), "baseline should not write .claude/"
        elif cond == "learning":
            assert opts.system_prompt == "", "learning should have empty system prompt"
            assert opts.setting_sources == ["project"], "learning needs setting_sources=['project']"
            settings_path = sandbox / ".claude" / "settings.json"
            assert settings_path.exists(), "learning sandbox missing .claude/settings.json"
            settings = json.loads(settings_path.read_text())
            assert settings.get("outputStyle") == "Learning", "learning settings.json missing outputStyle"
        elif cond == "regular":
            assert "pair programmer" in opts.system_prompt.lower(), "regular missing pair system prompt"
            assert opts.mcp_servers and MCP_SERVER_NAME in opts.mcp_servers, "regular missing MCP server"
            assert FULL_PROPOSE_TOOL_NAME in (opts.allowed_tools or []), "regular missing propose_options in allowed_tools"

        # Cleanup the temp sandbox so we don't leave dirs behind.
        import shutil
        shutil.rmtree(sandbox, ignore_errors=True)

    print("tutor_config self-test: OK")


def _self_test_student() -> None:
    """Verify the <done/> sentinel detection / stripping and that Student
    threads history correctly. No API calls."""

    # is_done: positive cases
    assert is_done("Looks good, we're done.\n<done/>")
    assert is_done("<done/>\n")
    assert is_done("yep\n  <done />  \n")  # whitespace and self-close variant
    # is_done: negative cases
    assert not is_done("not done yet")
    assert not is_done("the <done/> tag is in the middle of a line")  # no leading newline + trailing newline pattern

    # strip_done removes the sentinel but leaves the rest intact.
    assert strip_done("Looks good.\n<done/>") == "Looks good."
    assert strip_done("<done/>") == ""
    assert strip_done("Line 1\n<done/>\nLine 2") == "Line 1\nLine 2"

    # Student bookkeeping: history starts empty, first reply prepends the
    # problem prompt. We don't actually call the API; just inspect the
    # constructor and the user-content shape.
    s = Student(problem_prompt="Solve foo")
    assert s.history == []
    assert s.problem_prompt == "Solve foo"
    assert s.model.startswith("claude-haiku")
    assert s.system_prompt == STUDENT_SYSTEM_PROMPT

    print("student self-test: OK")


if __name__ == "__main__":
    # Bare invocation runs the in-process self-tests. Pass any other args to
    # invoke the CLI (e.g. `uv run run.py --condition regular -n 1`).
    if len(sys.argv) == 1:
        _self_test()
        _self_test_tutor_config()
        _self_test_student()
    else:
        sys.exit(main())
