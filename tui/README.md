# tui

TypeScript + Bun + Ink clone of the `claude` CLI, focused on the didactic
two-option pair-programming flow. Same stack the real CC uses (verified by
inspecting CC's compiled binary).

## Run it

```bash
cd tui
bun install   # first time only
bun start     # Ctrl-C / Ctrl-D quits
```

If `bun` isn't installed, fetch it from
<https://github.com/oven-sh/bun/releases/latest> (`bun-darwin-aarch64` for
macOS Apple Silicon).

Typecheck: `bun x tsc --noEmit`.

## Layout

```
src/
  index.tsx                  # entry: render(<App />)
  App.tsx                    # root: <Static> transcript + live region + input
  components/
    Entries.tsx              # UserLine, AssistantBlock, ToolPillRunning,
                             # ToolResult (collapsed past-tense or
                             # Update/Write block with synthesized diff),
                             # OptionsBlock, StepFooter, ErrorLine
    Markdown.tsx             # minimal markdown — inline `code`, **bold**,
                             # *italic*, ```diff fenced → DiffBlock
    Diff.tsx                 # unified-diff renderer with CC's Edit colors;
                             # cli-highlight Monokai theme; EditDiff +
                             # WriteDiff synthesize from old_string/new_string
    Input.tsx                # custom Ink useInput — handles batched stdin
                             # where Enter arrives as `\r` inside the input
                             # string (e.g. via tmux send-keys)
  agent/
    runner.ts                # long-running Session wrapping query() with an
                             # AsyncIterable<SDKUserMessage> queue so all
                             # turns share one conversation. Registers
                             # propose_options MCP tool, suppresses internal
                             # ToolSearch + propose_options validation errors
    systemPrompt.ts          # SYSTEM_PROMPT — keep in sync manually with
                             # experiments/web-prototype/server.py
```

## Why this stack

CC's actual stack is Bun-compiled TS + React 19 + Ink — we found `ink-box`,
`ink-text`, `react-dom@19`, and a `__BUN` segment in CC's binary. Earlier
Python attempts (Textual, prompt_toolkit, Rich) kept missing small details
that emerged from layout/rendering quirks specific to other frameworks. By
using the exact same primitives CC uses, a lot of behaviour (alt-screen
optionally, scrolling, terminal hyperlinks, focus, resize) comes for free.
