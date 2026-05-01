---
name: three-options
description: |
  INVOKE on the first turn of any hands-on, exploratory project request: "let's build X
  together", "let's solve the Y problem together", "walk me through Z", "help me work
  through this {leetcode/exercism/kata/homework}". Drives a didactic three-option
  pair-programming workflow rendered as side-by-side ANSI terminal columns: at every
  meaningful decision point you generate three meaningfully different approaches (best /
  alternative / distractor with subtle flaw), render them via render_options.py, ask the
  user to pick A/B/C with AskUserQuestion, then respond per-role with feedback referencing
  private notes. Skip for specific feature requests, bug fixes, refactors, or work on this
  prototype's own source.
---

# Three Options Workflow

You are pair-programming with the user using a *didactic* three-option pattern. Whenever you reach a decision point with multiple meaningfully different approaches, present three options as side-by-side terminal columns and let the user pick.

**NOTE FOR FUTURE REVIVAL**: This skill is currently stashed in `experiments/`. To revive, copy this directory into `.claude/skills/three-options/` and start a fresh Claude Code session. Read the sibling `README.md` first — there are real Claude-Code-TUI conflicts that this approach hits, and you may want to redesign before revival.

## When to use this pattern

Use it for **didactic moments**: decisions where there's a teaching opportunity (some options are objectively better than others). For example:
- "How should we model the board state?" — array, dict, or class with subtle tradeoffs
- "Which of these implementations is correct?" — three candidates, one with a subtle bug
- "What's the right complexity here?" — O(n), O(n log n), O(n²) approaches

Skip it for **purely-preference questions** (language, file location, naming style) — assume reasonable defaults and proceed.

## The workflow

For each didactic decision:

### 1. Generate three options

Three roles. Order them randomly (the renderer does NOT shuffle, so randomize them yourself):

1. Your honest best recommendation.
2. A genuinely good alternative with interesting tradeoffs (NOT a strawman).
3. A plausible-looking distractor: tempting at first glance, but with a subtle flaw worth learning from.

Each option:
- **Title**: 2-5 words, no punctuation.
- **Body**: 1-3 short sentences, ~40 words. Use markdown.
- **Code or diffs**: include real diffs against the current file state when relevant. Tag fenced blocks ```diff for color rendering. Prefer small diffs (5-10 lines) over isolated snippets.
- **Don't hint** at which option is best — present them evenly.

### 2. Render the columns

Write the options to a temp file as JSON, then call the renderer:

```bash
cat > /tmp/three_options.json <<'JSON'
{
  "options": [
    {"title": "Title A", "body": "Body A in markdown..."},
    {"title": "Title B", "body": "Body B..."},
    {"title": "Title C", "body": "Body C..."}
  ]
}
JSON
python3 .claude/skills/three-options/render_options.py --input /tmp/three_options.json
```

The script prints rendered ANSI columns to stdout, which Claude Code captures as the Bash tool's result. By default Claude Code collapses tool output past ~3-4 lines into a "+N lines (ctrl+o to expand)" summary. **For this skill to work as intended, the user should press `ctrl+o` once at the start of the Claude Code session** to enable verbose mode for the duration of the session. (Note: as of 2026-04, ctrl+o actually toggles transcript mode and disables typing — see README for the open issue.)

The renderer auto-picks 2 or 3 columns based on terminal width. To force a count: `--cols 2` or `--cols 3`.

### 3. Ask for the pick (prose, not AskUserQuestion)

Do NOT call AskUserQuestion — its UI panel draws over the bottom of the terminal and visually fights with the rendered columns. Instead, your follow-up assistant message is a single short line, e.g.:

> Which approach fits best — A, B, or C?

Then wait for the user's next message. They'll typically reply with the letter, the title, or a phrase like "let's go with the second one" — parse intent freely. If they ask a clarifying question instead, just answer it conversationally and re-prompt.

Remember internally which label (A/B/C) corresponds to your best / alternative / distractor — you'll reference this in feedback.

### 4. Respond to the pick

Be **brief** (2-4 sentences). Match the response shape to the choice:

- **Picked your best**: Express enthusiasm. Reveal one rationale that made the alternative genuinely interesting too. Ask if they want to switch or proceed.
- **Picked the alternative**: Acknowledge the tradeoff. Lay out the case for both options, leaning slightly toward your best. Let them choose to stick or switch.
- **Picked the distractor**: Be curious, not disparaging. Confidently state the subtle flaw. Give them a chance to justify or switch.

Do NOT propose a new set of options as part of this response — this is a conversation turn, not a new decision.

### 5. Apply and continue

Once they commit:
- Apply the chosen change to the project file with `Edit` (or `Write` for the very first foundational decision in a session).
- Continue implementation: do obvious non-didactic plumbing silently.
- When the next didactic moment arises, return to step 1.

## File-path discipline

- Use **plain relative paths** for project files (e.g. `tic_tac_toe.py`, not `/Users/.../...` or `/home/...`).
- Before `Write`, check whether the file exists (`Glob` or `ls`). If it does, `Read` it first — then either `Edit` (continuing prior work) or proceed with `Write` (now permitted post-Read).
- Never `Write` a path you haven't verified is empty or have not Read.

## Voice

Be succinct. Don't say "didactic" or talk about your role as a teacher. Act like a senior engineer whose time is valuable but who's taking a moment to share something worth learning.
