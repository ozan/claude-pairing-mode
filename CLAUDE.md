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

The TUI is split into two concerns. **`tui/src/core/`** is a generic
"minimal claude code clone" — chat shell, Session wrapping the SDK,
rendering primitives. **`tui/src/pair/`** is the choice-based
pair-programmer experiment layered on top via the `customToolHandlers`
extension hook + the App's generic `extra` event/entry slot. Iterating on
the experiment touches only `pair/`; iterating on the CC clone touches
only `core/`.

```
tui/
  src/
    index.tsx                # render(<PairApp />)
    core/
      App.tsx                # generic chat shell. Generic over ExtraEvent
                             #   and ExtraEntry so experiments can add
                             #   event/entry kinds without touching core.
                             #   <Static> transcript + live region +
                             #   bottom-anchored input with grey rule lines.
      Session.ts             # long-running Session<E> wrapping SDK query()
                             #   with an AsyncIterable user-message queue
                             #   so all turns share one conversation.
                             #   Routes assistant tool_use blocks named in
                             #   customToolHandlers to those handlers;
                             #   suppresses stream events + tool_results
                             #   for custom-handled and ToolSearch ids.
      types.ts               # CoreAgentEvent, ToolUseBlock,
                             #   CustomToolHandler<E>.
      components/
        Markdown.tsx         # inline `code`, **bold**, *italic*; ```diff
                             #   fences → DiffBlock. Parser always advances
                             #   per iteration (no infinite-loop on
                             #   unclosed backticks mid-stream).
        Diff.tsx             # unified-diff renderer with CC's captured
                             #   colors + cli-highlight (Monokai theme).
                             #   EditDiff + WriteDiff synthesize from
                             #   old_string/new_string.
        Input.tsx            # custom Ink useInput — handles batched stdin
                             #   where Enter arrives as `\r` inside the
                             #   input string (e.g. via tmux send-keys).
        Entries.tsx          # UserLine, AssistantBlock (`⏺ ` marker),
                             #   ToolPillRunning (animated dots), ToolResult
                             #   (collapses to `  Wrote N lines`, or
                             #   Update/Write with synthesized diff),
                             #   StepFooter, ErrorLine. Edit→Update rename.
    pair/
      systemPrompt.ts        # the didactic prompt.
      proposeOptions.ts      # propose_options MCP tool def, OptionsEvent
                             #   type, and the handler core invokes when
                             #   the assistant calls the tool.
      OptionsBlock.tsx       # two-column option panel.
      PairApp.tsx            # wires the experiment into core: constructs a
                             #   Session<OptionsEvent> with the MCP server
                             #   + system prompt + handler, mounts core
                             #   <App> with an `extra` slot that reduces
                             #   OptionsEvent → OptionsEntry → OptionsBlock.

experiments/
  web-prototype/             Stashed Python web UI (FastAPI + WebSocket,
                             marked.js + highlight.js). Same UX paradigm,
                             different surface. Its own README has run
                             instructions.
  three-options-skill/       Stashed Claude Code skill experiment. Paused
                             due to CC TUI rendering conflicts. Its README
                             has revival paths.
```

The pair experiment keeps its own copy of `SYSTEM_PROMPT` (in
`tui/src/pair/systemPrompt.ts`); the stashed web prototype keeps its own
in `experiments/web-prototype/server.py`. Edit either, copy by hand.

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

- TUI: `bun test` runs the suite (parser regressions, Session.translate, component renders). `bun x tsc --noEmit` for typecheck. Drive interactively in a terminal for end-to-end work; `tmux + send-keys` works for scripted tests but watch out — tmux delivers batched input where the Enter byte (`\\r`) is embedded in the input string. Our custom Input already handles this.
- Web: see `experiments/web-prototype/README.md`.

## Notable design decisions

- **Custom MCP tool over structured output via JSON schema**. The tool gives mechanical schema enforcement and a clean event channel; the runner suppresses the tool's content-block stream events and emits a synthesized `options` event so the UI doesn't see the underlying tool plumbing.
- **Plain-text user replies after options**, not `AskUserQuestion`-style multi-choice. Users type "A" / "B" / "the second one" — Claude parses intent.
- **Model-driven option ordering**, not server-side shuffle. The model's `private_notes.best_index` would point to the wrong column if we shuffled.
- **Same Ink primitives CC uses for the TUI**. Verified by inspecting CC's compiled binary (`__BUN` segment + strings showing `ink-box`, `react-dom@19`, etc.). Approximating from Python kept missing small details.
