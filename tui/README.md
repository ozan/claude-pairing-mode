# tui

TypeScript + Bun + Ink clone of the `claude` CLI, with the didactic
two-option pair-programming flow as a layered experiment on top.

The codebase is split into two clear pieces:

- **`src/core/`** — minimal `claude` clone. Generic chat shell, Session
  wrapping the SDK, all the rendering primitives (Markdown, Diff, tool
  pills, footer). Knows nothing about propose_options. Could host a
  different experiment on top.
- **`src/pair/`** — the choice-based pair-programmer experiment: the
  `propose_options` MCP tool, the system prompt, the 2-column OptionsBlock,
  and a thin `PairApp` that wires the experiment into core via
  `customToolHandlers` + the App's `extra` extension hook.

`src/index.tsx` just renders `<PairApp />`. To iterate on the experiment,
touch only `src/pair/`. To improve the underlying CC clone, touch only
`src/core/`.

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
Tests: `bun test` — 76 passing across 7 files.

