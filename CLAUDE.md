# ai-pair-proto

Prototype of a didactic *two-option* pair-programming UI. Claude proposes two approaches to each meaningful coding decision (one honest best, one plausible-looking distractor with a subtle flaw); the user picks; Claude responds per-role and applies the change to a real file. The point of the experiment is to make every code change something the user has *seen and chosen*, building familiarity through small didactic decisions.

The active surface is the **TS/Bun/Ink TUI** (`tui/`) — same stack the real `claude` CLI uses (Bun runtime, React 19 + Ink, `@anthropic-ai/claude-agent-sdk`), discovered by inspecting CC's compiled binary. An earlier Python web prototype (`experiments/web-prototype/`) is stashed for reference but no longer iterated on.

## Run it

```bash
cd tui && bun start
```
Quit with Ctrl-C / Ctrl-D. Restart after edits to source.

If `bun` isn't installed: download `bun-darwin-aarch64` from <https://github.com/oven-sh/bun/releases/latest> and put it in your PATH.

The web prototype still works if you want to compare; see `experiments/web-prototype/README.md`.

## Architecture (active TUI)

```
tui/             Bun + React 19 + Ink CLI clone of `claude`. Owns
                    SYSTEM_PROMPT and the propose_options MCP tool — the
                    Python web prototype keeps its own copy in
                    experiments/web-prototype/server.py; if you edit either
                    SYSTEM_PROMPT, copy the change to the other.
                    - src/index.tsx:  render(<App />). No alt-screen — content
                      flows into terminal scrollback so mouse-wheel/page-up
                      work.
                    - src/App.tsx:  ChatApp root. <Static> for committed past
                      entries (Ink writes them once, never re-renders, so
                      layout can't corrupt while streaming); live region below
                      for the currently-streaming assistant block / running
                      tool pill; input row pinned at the bottom with thin
                      grey rule lines above and below.
                    - src/agent/runner.ts:  long-running Session. Wraps query()
                      with an AsyncIterable<SDKUserMessage> queue so all turns
                      share one conversation — the model remembers prior
                      turns. Filters internal SDK ToolSearch events;
                      suppresses propose_options tool_results (whether
                      success-stub or zod validation failure) so the model
                      can retry malformed calls without leaking errors into
                      the transcript.
                    - src/agent/systemPrompt.ts:  SYSTEM_PROMPT for the TUI.
                      Keep in sync manually with the web prototype's copy if
                      you edit either.
                    - src/components/Diff.tsx:  unified-diff renderer with CC's
                      captured colors + cli-highlight (Monokai-ish theme tuned
                      to CC's palette). EditDiff/WriteDiff synthesize a
                      unified diff from the SDK's old_string/new_string for
                      inline Update/Write rendering.
                    - src/components/Markdown.tsx:  inline `code`, **bold**,
                      *italic*; ```diff fences → DiffBlock. Critical: parser
                      always advances `i` per loop iteration so an unclosed
                      streamed backtick doesn't infinite-loop.
                    - src/components/Entries.tsx:  UserLine, AssistantBlock
                      (with `⏺ ` marker), ToolPillRunning (animated dots),
                      ToolResult (collapses to `  Wrote N lines` etc., or
                      Update/Write block with synthesized diff), OptionsBlock
                      (two-column flex), StepFooter, ErrorLine. Tool name
                      `Edit` is renamed to `Update` to match CC.
                    - src/components/Input.tsx:  custom input on Ink's
                      useInput — handles batched stdin where Enter arrives
                      as `\\r` embedded in the input string (e.g. via tmux
                      send-keys), not as a separate key event.
                    - package.json + bun.lock:  Bun project. Deps: ink 7,
                      react 19, @anthropic-ai/claude-agent-sdk, chalk,
                      cli-highlight, @inkjs/ui, ink-syntax-highlight.

experiments/
  web-prototype/    Stashed Python web UI (FastAPI + WebSocket, marked.js +
                    highlight.js). Same UX paradigm, different surface. Its
                    own README has run instructions.
  three-options-skill/   Stashed Claude Code skill experiment. Paused due to
                         CC TUI rendering conflicts. Its README has revival
                         paths.
```

## Conventions

- **Diff format (REQUIRED for code options)**: option bodies use ` ```diff ` fences containing unified-diff format with `+++ <filename>` header AND a `@@ -OLD,_ +NEW,_ @@` hunk header. The renderer uses the hunk header for line numbers and the `+++` filename for syntax-highlighter language detection.
- **File-path discipline**: relative paths only (`tic_tac_toe.py`, never absolute). Before `Write`, check existence (`Glob` / `ls`) and `Read` if it exists; `Edit` thereafter.
- **Permission mode**: `bypassPermissions` (no approval prompts; POC choice, not appropriate for shared use).
- **Model**: Opus 4.7 default; `effort` and `thinking` are SDK defaults (adaptive). Opus is worth the latency vs Haiku for the didactic option quality.

## What's working

- Two options, model-orders the columns (no server-side shuffling — the model's `private_notes.best_index` references the same indices the user sees).
- Streaming markdown with diffs and syntax highlighting.
- Tool-use pills with animated progress, collapsed tool results, `● Update(filepath)` / `● Write(filepath)` blocks with synthesized inline diffs.
- Session memory across turns (long-running Session wraps one SDK query()).
- Native terminal scrolling (no alt-screen) — mouse wheel / page-up just work.

## What's still rough

- No interrupt button. Once a turn starts, no way to cancel.
- No spend/turn caps (`max_budget_usd`, `max_turns` unset).
- Syntax-highlight palette is Monokai-ish, close to CC but not pixel-exact. CC has access to file context for diffs (showing surrounding unchanged lines); we only have the SDK's old_string/new_string.

## Testing notes

- TUI: `bun x tsc --noEmit` for typecheck. Drive interactively in a terminal; `tmux + send-keys` works for scripted tests but watch out — tmux delivers batched input where the Enter byte (`\\r`) is embedded in the input string. Our custom Input already handles this.
- Web: see `experiments/web-prototype/README.md`.

## Notable design decisions

- **Custom MCP tool over structured output via JSON schema**. The tool gives mechanical schema enforcement and a clean event channel; the runner suppresses the tool's content-block stream events and emits a synthesized `options` event so the UI doesn't see the underlying tool plumbing.
- **Plain-text user replies after options**, not `AskUserQuestion`-style multi-choice. Users type "A" / "B" / "the second one" — Claude parses intent.
- **Model-driven option ordering**, not server-side shuffle. The model's `private_notes.best_index` would point to the wrong column if we shuffled.
- **Same Ink primitives CC uses for the TUI**. Verified by inspecting CC's compiled binary (`__BUN` segment + strings showing `ink-box`, `react-dom@19`, etc.). Approximating from Python kept missing small details.
