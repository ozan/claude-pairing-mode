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

## Layout

```
src/
  index.tsx                            # render(<PairApp />)
  core/
    App.tsx                            # generic chat shell. Generic over
                                       #   ExtraEvent (E) and ExtraEntry (X)
                                       #   so experiments can add their own
                                       #   event/entry kinds without modifying
                                       #   core. Renders <Static> transcript +
                                       #   live region + bottom-anchored input.
    Session.ts                         # long-running Session<E> wrapping SDK
                                       #   query() with an AsyncIterable
                                       #   message queue. Dispatches custom
                                       #   tool calls to user-supplied
                                       #   `customToolHandlers`. Suppresses
                                       #   stream events + tool_results for
                                       #   custom-handled (and ToolSearch)
                                       #   tool ids.
    types.ts                           # CoreAgentEvent + ToolUseBlock +
                                       #   CustomToolHandler<E>
    components/
      Markdown.tsx                     # inline `code`, **bold**, *italic*;
                                       #   ```diff fences → DiffBlock
      Diff.tsx                         # unified-diff renderer. EditDiff +
                                       #   WriteDiff synthesize from
                                       #   old_string/new_string. Monokai
                                       #   syntax highlighting via
                                       #   cli-highlight.
      Input.tsx                        # custom Ink useInput. Handles batched
                                       #   stdin where Enter arrives as `\r`
                                       #   inside the input string (e.g. via
                                       #   tmux send-keys).
      Entries.tsx                      # UserLine, AssistantBlock,
                                       #   ToolPillRunning, ToolResult,
                                       #   StepFooter, ErrorLine. The Update
                                       #   (Edit) and Write tool results
                                       #   render with synthesized inline
                                       #   diffs.
  pair/
    proposeOptions.ts                  # propose_options MCP tool definition,
                                       #   OptionsEvent type, the
                                       #   proposeOptionsHandler that core's
                                       #   Session calls when the model
                                       #   invokes the tool.
    OptionsBlock.tsx                   # two-column option panel.
    PairApp.tsx                        # wires the experiment: constructs a
                                       #   Session<OptionsEvent> with the pair
                                       #   MCP server + system prompt + the
                                       #   handler, mounts core <App> with an
                                       #   `extra` extension that reduces an
                                       #   OptionsEvent to an OptionsEntry and
                                       #   renders it via OptionsBlock.
    systemPrompt.ts                    # the didactic prompt.
```

## Extension model

When you want to add a feature to the **experiment** (the choice-based pair
programmer), you almost always touch only `src/pair/`:

- New event kind from a custom tool? Add it to `OptionsEvent`'s union, emit
  it from the handler, render it in `PairApp.tsx`'s `extra`.
- New rendering for `options`? Edit `OptionsBlock.tsx`.
- Different system prompt? Edit `systemPrompt.ts`.
- Different MCP tool schema? Edit `proposeOptions.ts`.

When you want to improve the **core CC clone** (rendering quality,
performance, new built-in feature), touch only `src/core/`:

- Tool result formatting? Edit `core/components/Entries.tsx`.
- Markdown / diff rendering? Edit the corresponding component.
- How a Session handles a generic SDK message type? Edit `Session.translate`.

## Tests

`bun test` runs the suite in <1s:

- `core/components/__tests__/Markdown.test.ts` — splitInline, splitBlocks,
  isDiffBlock. Includes regressions for the unclosed-backtick infinite-loop
  bug we hit while streaming.
- `core/components/__tests__/Diff.test.ts` — parse, detectLang.
- `core/components/__tests__/Entries.test.ts` — summarizeInput, shortToolName.
- `core/components/__tests__/Entries.render.test.tsx` — ink-testing-library
  renders of every core entry component.
- `core/__tests__/Session.test.ts` — Session.translate driven with synthetic
  SDK messages (text streaming, regular tools, ToolSearch hidden, result,
  customToolHandlers extension).
- `pair/__tests__/proposeOptions.test.ts` — proposeOptionsHandler in
  isolation + Session integration (well-formed call → options event,
  malformed → silent suppression, stream events suppressed).
- `pair/__tests__/OptionsBlock.test.tsx` — render of the 2-column option
  panel.
