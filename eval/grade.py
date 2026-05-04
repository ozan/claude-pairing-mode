"""Grade a tagged eval run via Opus-as-judge.

  uv run --env-file .env grade.py runs/initial
  uv run --env-file .env grade.py runs/initial --baseline runs/baseline
  uv run --env-file .env grade.py runs/initial --only leetcode-two-sum --force

For each <slug>/transcript.md inside the run dir, we send the transcript to
Opus with the rubric prompt and get back per-criterion scores (1-5) plus
short rationales. Results land at <slug>/grade.json plus an aggregate
grades_summary.json at the run-dir root.

Methodology mirrors the TS grader (tui/src/eval/grader.ts) so scores
remain comparable across the migration:
  - 4 pedagogical criteria graded from the experiment alone
  - 2 productivity criteria graded against an optional baseline transcript
  - For baseline-condition runs themselves, productivity pins to 3 (a
    baseline is the reference, not something to compare against itself)
  - Weighted to a single 1-5 score, then normalized to 0-1
  - One JSON-parse retry with stricter wording on schema violations

The grader uses the raw Anthropic API (one shot per transcript). No agent
harness, no streaming.
"""

import argparse
import asyncio
import dataclasses
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from anthropic import AsyncAnthropic


DEFAULT_GRADER_MODEL = "claude-opus-4-7"

GRADER_SYSTEM_PROMPT = """
You are an expert evaluator of pair-programming sessions. You are reviewing transcripts of conversations between an AI pair-programming assistant ("Pair") and a junior software engineer ("User"). The Pair's goal is BOTH to help solve the problem AND to teach the user something useful along the way (didactic pair-programming).

You will see one transcript from the experiment under review ("EXPERIMENT"). You may also see a transcript from a BASELINE run on the same problem where the Pair had no special instructions — this establishes a productivity reference point.

Score the EXPERIMENT on 7 criteria, each on a 1–5 integer scale. Use the anchors below; calibrate to them rather than to your priors.

== PEDAGOGICAL VALUE (judge from EXPERIMENT alone) ==

1. question_frequency - How many times does the pair engage the user with didactic questions at teachable moments (subtleties, classic gotchas, trade-offs, idioms worth knowing)?
   1: few didactic questions, mostly code-writing or clarifying questions with few teachable moments
   3: at least some effort by the pair to question the user with pedagogical intentenio
   5: high frequency of questioning, with most meaningful decision points involving the user

2. question_quality — When the Pair frames a choice (or surfaces a fork), does it hit the CRUX of the problem (boundary conditions, algorithmic trade-offs, design tensions)?
   1: choices are cosmetic, trivial, or absent.
   3: at least one substantive choice; others surface or are missed.
   5: choices consistently target the most consequential parts of the problem space.

3. scaffolding - Is the sequence of questions well scaffolded, with a logical progression, a smooth difficulty gradient, and no spoilers?
   1: too few questions, answers revealed/hinted or too obvious, or major jumps in difficulty
   3: reasonable scaffolding with no spoilers, but some abrupt skill or domain jumps
   5: pedagogically perfect scaffolding

4. flow_and_tone - Does the pair provide useful and actionable guidance, and engage in natural back and forth with the user, resulting in good conversational flow?
   1: bad conversational dynamic, excessive conflict, non sequiturs or unactionable or irrelevant responses
   3: tone is warm but conversational flow is not fluid
   5: conversational flow is natural and reflects an ideal pedagogical experience for both participants


== PRODUCTIVITY (compare EXPERIMENT to BASELINE if present) ==

5. effectiveness — Does the EXPERIMENT's final code correctly solve the original problem, in a manner equivalent to the baseline?
   1: broken, missing requirements, or never converges, or is significantly better than the baseline
   3: generally works and comparable to baseline
   5: an ideal solution, noticeably better than the baseline

6. friction — Was the conversation efficient given the problem and given the BASELINE reference?
   With BASELINE: penalize taking substantially longer (turns or prose volume) without a proportional pedagogical payoff.
   1: 2x+ longer than baseline with no proportional teaching gain.
   3: comparable to baseline OR only slighly longer with proportional payoff.
   5: tighter than baseline, or substantially better teaching for modest extra length.
   Without BASELINE: judge friction in absolute terms (3 = average for the problem class).

Be specific in rationales — name the moments you're scoring on. Each rationale should be 1–3 sentences. No flattery, no hedging language; act as a calibrated reviewer.

Output a SINGLE JSON object with this exact shape — no prose outside the JSON, no markdown fence:

{
  "pedagogical": {
    "question_frequency": { "score": 1-5, "rationale": "..." },
    "question_quality":   { "score": 1-5, "rationale": "..." },
    "scaffolding":        { "score": 1-5, "rationale": "..." },
    "flow_and_tone":      { "score": 1-5, "rationale": "..." }
  },
  "productivity": {
    "effectiveness":      { "score": 1-5, "rationale": "..." },
    "friction":           { "score": 1-5, "rationale": "..." }
  }
}
""".strip()


# Per-criterion weights (sum to 1). Edit to re-balance.
SCORE_WEIGHTS = {
    "question_frequency": 0.3,
    "question_quality":   0.1,
    "scaffolding":        0.1,
    "flow_and_tone":      0.1,
    "effectiveness":      0.2,
    "friction":           0.2,
}

PEDAGOGICAL_KEYS = ("question_frequency", "question_quality", "scaffolding", "flow_and_tone")
PRODUCTIVITY_KEYS = ("effectiveness", "friction")


# ---------- pure helpers ----------

def extract_json(text: str) -> str:
    """Best-effort JSON extraction. Strips a ```json fence if present, else
    grabs the substring from the first `{` to the matching last `}`. Models
    sometimes emit a 'Here is my evaluation:' preamble that strict
    json.loads() would reject."""
    s = text.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", s)
    if fence:
        return fence.group(1).strip()
    first = s.find("{")
    last = s.rfind("}")
    if first != -1 and last > first:
        return s[first:last + 1]
    return s


def validate_grade(parsed: Any) -> dict | None:
    """Strictly validate AND normalize. Drops any extra fields the grader
    invented (e.g. `scaffolding_note`); returns None if any required field
    is missing or non-numeric."""
    if not isinstance(parsed, dict):
        return None
    peds = parsed.get("pedagogical")
    prods = parsed.get("productivity")
    if not isinstance(peds, dict) or not isinstance(prods, dict):
        return None
    out_peds = {}
    for k in PEDAGOGICAL_KEYS:
        c = peds.get(k)
        if not isinstance(c, dict) or not isinstance(c.get("score"), (int, float)):
            return None
        out_peds[k] = {"score": c["score"], "rationale": str(c.get("rationale", ""))}
    out_prods = {}
    for k in PRODUCTIVITY_KEYS:
        c = prods.get(k)
        if not isinstance(c, dict) or not isinstance(c.get("score"), (int, float)):
            return None
        out_prods[k] = {"score": c["score"], "rationale": str(c.get("rationale", ""))}
    return {"pedagogical": out_peds, "productivity": out_prods}


def pin_baseline_productivity(grade: dict) -> dict:
    """For baseline-condition runs, productivity criteria are mechanically
    pinned to 3. They're the reference, so judging them comparatively makes
    no sense."""
    pinned = json.loads(json.dumps(grade))  # deep copy
    for k in PRODUCTIVITY_KEYS:
        pinned["productivity"][k] = {
            "score": 3,
            "rationale": "(pinned to 3 — this is the baseline reference run)",
        }
    return pinned


def weighted_score(grade: dict) -> float:
    return sum(
        grade["pedagogical" if k in PEDAGOGICAL_KEYS else "productivity"][k]["score"] * w
        for k, w in SCORE_WEIGHTS.items()
    )


def normalized_score(grade: dict) -> float:
    """Linear (raw - min) / (max - min) on the 1-5 scale → 0-1."""
    return (weighted_score(grade) - 1) / 4


# ---------- grader API call ----------

async def call_grader(client: AsyncAnthropic, prompt: str, model: str) -> str:
    # 8192 instead of 4096: long propose_options runs (e.g. tic-tac-toe with
    # 6 options × full rationales) overflow Opus's response at 4096 and the
    # JSON parse fails mid-string.
    response = await client.messages.create(
        model=model,
        max_tokens=8192,
        system=GRADER_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in response.content if b.type == "text")


async def grade_transcript(
    client: AsyncAnthropic,
    experiment_md: str,
    baseline_md: str | None,
    model: str,
) -> tuple[dict, str]:
    """Send one transcript (and optional baseline) to the grader. One retry
    with stricter wording if the JSON is malformed or missing/extra fields.
    Returns (validated_grade, raw_grader_text). Raises on hard failure."""
    sections = []
    if baseline_md:
        sections.append(f"# BASELINE TRANSCRIPT (no system prompt, no didactic tools)\n\n{baseline_md}")
    sections.append(f"# EXPERIMENT TRANSCRIPT (under review)\n\n{experiment_md}")
    sections.append("# YOUR TASK\n\nGrade the EXPERIMENT against the rubric. Return JSON only.")
    base_prompt = "\n\n---\n\n".join(sections)

    async def attempt(prompt: str) -> tuple[dict | None, str]:
        raw = await call_grader(client, prompt, model)
        cleaned = extract_json(raw)
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            return None, raw
        return validate_grade(parsed), raw

    grade, raw1 = await attempt(base_prompt)
    if grade:
        return grade, raw1

    # Retry with stricter wording. Common failures: omitting one criterion,
    # or inventing fields like `scaffolding_note`.
    strict = (
        "\n\n# REMINDER (strict)\n\nReturn EXACTLY the schema shown — no extra "
        "keys (e.g. no `scaffolding_note`), no missing keys, all 4 pedagogical + "
        "2 productivity criteria with numeric scores. JSON object only."
    )
    grade2, raw2 = await attempt(base_prompt + strict)
    if grade2:
        return grade2, raw2

    preview = (raw2 or raw1)[:400].replace("\n", "\\n")
    raise RuntimeError(f"grader output unusable after 2 attempts. Raw (first 400 chars): {preview}")


# ---------- run-dir orchestration ----------

@dataclass
class GradedRun:
    slug: str
    weighted: float
    normalized: float
    is_baseline: bool


GRADER_TRANSCRIPT_FILENAME = "transcript_grader.md"


def discover_runs(run_dir: Path) -> list[Path]:
    """Return per-problem dirs (those with a grader-view transcript)."""
    return sorted(
        p for p in run_dir.iterdir()
        if p.is_dir() and (p / GRADER_TRANSCRIPT_FILENAME).exists()
    )


def is_baseline_run(run_dir: Path) -> bool:
    """Read config.json to determine whether the run is the baseline condition."""
    cfg_path = run_dir / "config.json"
    if not cfg_path.exists():
        return False
    try:
        cfg = json.loads(cfg_path.read_text())
        return cfg.get("condition") == "baseline"
    except (json.JSONDecodeError, OSError):
        return False


async def grade_one(
    client: AsyncAnthropic,
    problem_dir: Path,
    baseline_md: str | None,
    is_baseline: bool,
    model: str,
    force: bool,
) -> GradedRun | None:
    grade_path = problem_dir / "grade.json"
    if grade_path.exists() and not force:
        cached = json.loads(grade_path.read_text())
        return GradedRun(
            slug=problem_dir.name,
            weighted=cached["weighted"],
            normalized=cached["normalized"],
            is_baseline=cached.get("is_baseline", False),
        )

    experiment_md = (problem_dir / GRADER_TRANSCRIPT_FILENAME).read_text()
    grade, raw = await grade_transcript(client, experiment_md, baseline_md, model)
    if is_baseline:
        grade = pin_baseline_productivity(grade)

    weighted = weighted_score(grade)
    normalized = normalized_score(grade)

    grade_path.write_text(json.dumps({
        "slug": problem_dir.name,
        "is_baseline": is_baseline,
        "model": model,
        "graded_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "grade": grade,
        "weighted": weighted,
        "normalized": normalized,
        "raw_response": raw,
    }, indent=2))

    return GradedRun(
        slug=problem_dir.name, weighted=weighted, normalized=normalized,
        is_baseline=is_baseline,
    )


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("run_dir", help="Run dir to grade (e.g. runs/initial)")
    p.add_argument("--baseline", default=None,
                   help="Baseline run dir for productivity comparison.")
    p.add_argument("--only", default=None, help="Grade only this slug.")
    p.add_argument("-f", "--force", action="store_true",
                   help="Re-grade even if grade.json already exists.")
    p.add_argument("--model", default=DEFAULT_GRADER_MODEL)
    p.add_argument("-j", "--concurrency", type=int, default=4,
                   help="Grade this many transcripts in parallel. Each grade is "
                        "one async API call, so concurrency is cheap. Beware "
                        "Anthropic rate limits at high N.")
    return p.parse_args(argv)


async def _main_async(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    if not run_dir.is_dir():
        print(f"not a directory: {run_dir}", file=sys.stderr)
        return 2

    is_baseline = is_baseline_run(run_dir)
    baseline_dir = Path(args.baseline) if args.baseline else None

    if is_baseline and baseline_dir:
        print("note: --baseline ignored — this run IS the baseline.")
        baseline_dir = None

    problem_dirs = discover_runs(run_dir)
    if args.only:
        problem_dirs = [p for p in problem_dirs if p.name == args.only]
        if not problem_dirs:
            print(f"no run dir matches --only {args.only}", file=sys.stderr)
            return 2

    print(
        f"grading {len(problem_dirs)} run(s) in {run_dir}  "
        f"baseline={'yes' if is_baseline else 'no'}  "
        f"compare-against={baseline_dir or 'none'}  model={args.model}"
    )

    client = AsyncAnthropic()
    n_total = len(problem_dirs)
    semaphore = asyncio.Semaphore(max(1, args.concurrency))
    completed = 0

    async def grade_with_progress(idx: int, pdir: Path) -> GradedRun | None:
        nonlocal completed
        async with semaphore:
            baseline_md: str | None = None
            if baseline_dir:
                bpath = baseline_dir / pdir.name / GRADER_TRANSCRIPT_FILENAME
                if bpath.exists():
                    baseline_md = bpath.read_text()
                else:
                    print(f"  (no baseline transcript at {bpath} for {pdir.name} — grading without)")
            try:
                r = await grade_one(client, pdir, baseline_md, is_baseline, args.model, args.force)
            except Exception as e:
                completed += 1
                print(f"  ✗ [{completed}/{n_total}] {pdir.name}: grader failed: {type(e).__name__}: {e}")
                return None
            completed += 1
            if r:
                print(f"  ✓ [{completed}/{n_total}] {pdir.name}: weighted={r.weighted:.2f}  normalized={r.normalized:.2f}")
            return r

    raw_results = await asyncio.gather(
        *(grade_with_progress(i, p) for i, p in enumerate(problem_dirs))
    )
    results: list[GradedRun] = [r for r in raw_results if r is not None]

    if not results:
        print("\nno successful grades.")
        return 1

    mean_weighted = sum(r.weighted for r in results) / len(results)
    mean_normalized = sum(r.normalized for r in results) / len(results)

    summary = {
        "run_dir": str(run_dir),
        "is_baseline": is_baseline,
        "baseline_compared_against": str(baseline_dir) if baseline_dir else None,
        "n": len(results),
        "mean_weighted": mean_weighted,
        "mean_normalized": mean_normalized,
        "graded_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "model": args.model,
        "results": [dataclasses.asdict(r) for r in results],
    }
    (run_dir / "grades_summary.json").write_text(json.dumps(summary, indent=2))

    print(
        f"\nMean across {len(results)} run(s): "
        f"weighted={mean_weighted:.2f} (1-5)  normalized={mean_normalized:.2f} (0-1)"
    )
    print(f"Summary: {run_dir / 'grades_summary.json'}")
    return 0


def main(argv: list[str] | None = None) -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY (the grader uses the raw API).", file=sys.stderr)
        return 2
    args = _parse_args(argv if argv is not None else sys.argv[1:])
    return asyncio.run(_main_async(args))


if __name__ == "__main__":
    sys.exit(main())
