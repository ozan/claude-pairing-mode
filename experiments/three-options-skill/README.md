# three-options-skill (paused experiment)

This is a stashed Claude Code skill that attempted to bring this repo's web-prototype "didactic two-/three-option pair-programming" UI directly into Claude Code itself, so the user wouldn't need to switch to a separate web UI.

We paused it (April 2026) because of fundamental conflicts with Claude Code's TUI rendering. The intent here is not to throw it away — it's a stash for possible revival when conditions change (Claude Code adds expansion controls, or a different rendering channel emerges).

## What's in this directory

- `SKILL.md` — the skill's frontmatter + workflow doc. Designed to be auto-invoked when the user opens a hands-on coding session.
- `render_options.py` — a Python script that takes JSON of options and renders them as side-by-side ANSI columns in the terminal, with diff coloring inside fenced ```diff blocks.

## Why we paused

We tried several rendering strategies inside Claude Code. Each hit a different wall:

1. **`Bash` tool with column-rendered ANSI output** (the saved approach above). Claude Code's TUI collapses tool stdout past ~3-4 lines into a `+N lines (ctrl+o to expand)` summary. There's no documented setting to disable this (open issues #12589, #25776, #10636, #39683).
2. **Bypass the capture by writing to `/dev/tty`**. Works mechanically — output reaches the user's terminal — but Claude Code's TUI doesn't know about our writes and continues drawing its own UI elements (the `(No output)` placeholder, AskUserQuestion popovers, etc.) on top of our content. Result: visual interleaving / overwrites.
3. **Markdown tables in the assistant response**. Renders cleanly but markdown tables can't contain fenced code blocks in cells, so options can't include diffs. Title-only summaries side-by-side worked but lost the value of seeing the actual code.
4. **Real `Edit` calls on temp files** (no rendering script). Each option becomes a real Edit-tool diff on a temp file, so the user sees Claude Code's native diff renderer per option. Visually correct but adds 6+ tool calls per decision (3 Writes + 3 Edits) and shows the "before" state three times. Heavy.
5. **`ctrl+o` workarounds.** `ctrl+o` actually toggles *transcript mode* (a less-like read-only view) — typing is disabled inside it. Per-call expansion shows the *whole tool call including the heredoc command source*, not just the output.

The deeper finding (from research into Claude Code's compiled binary): tool-output rendering is **dispatched by tool name** in the TUI. `Edit`/`Read`/`Write` go through structured-data renderers that show full content; `Bash` goes through a "collapse if long" path. This is hard-coded; no plugin/hook/setting alters it.

## Possible revival paths

Roughly in order of likelihood-to-succeed:

1. **Wait for a configurable threshold.** If Claude Code adds a setting like `bashOutputMaxLines` or `outputCollapseThreshold`, the column-rendering approach (this directory's code) starts working immediately.
2. **Plugin with `UserPromptSubmit` hook.** Claude Code plugins can register hooks that inject `additionalContext`. A hook that injects skill guidance per turn would mimic a system prompt, making the skill more reliably invoked. Wouldn't fix the rendering, but might be combined with #4 below.
3. **MCP tool with rich content type.** The MCP spec allows non-text content types. If Claude Code's TUI ever renders MCP tool results expanded by default (or with image/embedded-resource content), we might get our columns through that channel.
4. **Edit-on-temp-files approach.** Already known to work; the open question is whether 6 tool calls per decision is acceptable. If we accept it, we get pixel-perfect native rendering today. The skill would need rewriting around `Edit` instead of `Bash + render_options.py`.
5. **Render to a separate terminal pane** via `tmux` or `screen` integration. Too clunky for general use, but possible if the user has tmux.

## How to revive

```bash
# From the repo root:
mkdir -p .claude/skills
cp -r experiments/three-options-skill .claude/skills/three-options

# Then start a fresh Claude Code session in this directory.
# The skill will be auto-loaded based on its frontmatter description.
```

You may also need a `CLAUDE.md` instruction nudging Claude to invoke this skill on relevant prompts (skill descriptions alone don't always trigger reliably).

## Related

- Live in-development version: the web prototype in `server.py` + `static/index.html` (project root). That version doesn't have these TUI constraints.
