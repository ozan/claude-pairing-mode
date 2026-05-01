# ai-pair-proto

Web prototype of a didactic *two-option* pair-programming UI. Claude proposes two approaches to each meaningful coding decision (one honest best, one plausible-looking distractor with a subtle flaw); the user picks; Claude responds per-role and applies the change to a real file. The point of the experiment is to make every code change something the user has *seen and chosen*, building familiarity through small didactic decisions.

## Run it

```bash
uv run uvicorn server:app --host 127.0.0.1 --port 8000 --log-level warning
```

Open http://127.0.0.1:8000. WebSocket-driven; no `--reload` flag (it kills WS mid-turn). Bounce manually after `server.py` edits.

## Architecture

```
server.py        FastAPI app + /ws WebSocket endpoint.
                 - Custom MCP tool propose_options (in-process via claude-agent-sdk's
                   create_sdk_mcp_server / @tool). Schema: { options: [2], private_notes:
                   { best_index, trap_flaw } }.
                 - Per-WS Connection: tracks suppression of stream events for our
                   tool's content blocks; scrubs private_notes from forwarded events;
                   emits a synthesized {type: "options"} event with the public option
                   payload.
                 - SYSTEM_PROMPT defines the didactic-vs-clarifying distinction, the
                   "best + distractor" framing, the model-driven order randomization,
                   the prose-reply selection mechanic, and the per-role response shape.
                 - Wire format (server -> browser) follows Claude Code's `stream-json`
                   shape: stream_event / assistant / user / result / system, plus our
                   custom `options` and `error`.

static/index.html   Single-page UI.
                    - WS client.
                    - Renders options as 2 side-by-side cards (Option A / Option B).
                    - No click selection; user types A/B/letters/phrases in the
                      textarea. Server forwards plain text to Claude.
                    - marked.js + highlight.js (github-dark theme) for streaming
                      markdown rendering. Re-renders on every text_delta so elements
                      materialize as syntax completes (Claude-Code feel).
                    - Custom diff rendering matched pixel-for-pixel to Claude Code's
                      Edit-tool diffs: backgrounds rgb(2,40,0)/rgb(61,1,0); fg
                      rgb(80,200,80)/rgb(220,90,90); off-white context lines; cyan-blue
                      hunk headers; line numbers parsed from @@ -OLD,_ +NEW,_ @@; per-line
                      hljs syntax highlighting via `:where()` rules so hljs token colors
                      override the line's diff fg while the line bg is preserved.
                    - Tool-call pills (⏺ Bash(...), ⏺ Edit(...), etc.) for non-propose
                      tools. Tool-result expandable summaries.
                    - Whimsical loader rotates "Pondering…" / "Cogitating…" / etc. on
                      ~2.2s tick.

pyproject.toml + uv.lock   uv project. Python 3.14. Deps: claude-agent-sdk, fastapi,
                            uvicorn[standard].

experiments/three-options-skill/   Stashed Claude Code skill from a parallel attempt to
                                   bring this UI inside Claude Code itself. Paused due to
                                   TUI conflicts. See its README.md for revival paths.
```

## Conventions

- **Diff format (REQUIRED)**: option bodies for code changes use ` ```diff ` fences containing unified-diff format with `+++ <filename>` header AND a `@@ -OLD,_ +NEW,_ @@` hunk header. The renderer needs the hunk header to source line numbers. The `+++ filename` is what the renderer uses to detect the hljs language.
- **File-path discipline**: relative paths only (`tic_tac_toe.py`, never `/Users/.../...` or `/home/.../...`). Before `Write`, check existence (`Glob` / `ls`) and `Read` if it exists; `Edit` thereafter.
- **Permission mode**: `bypassPermissions` (no approval prompts; convenient for POC, would not be appropriate for shared use).
- **Model**: Opus 4.7 default; `effort` and `thinking` are SDK defaults (adaptive). We tried Haiku for speed but it produced lower-quality didactic options — Opus is worth the latency.

## What's working

- Two options, model-orders the columns (no server-side shuffling — the model's `private_notes.best_index` references the same indices the user sees).
- Streaming markdown with live re-render and syntax highlighting.
- Diff rendering that matches Claude Code's Edit-tool output: line numbers, exact colors, hljs tokens inside `+`/`-`/context lines.
- Tool-use pills, tool-result summaries (click to expand).
- Whimsical rotating loader.
- Test starters in the UI: Tic-tac-toe, Staircase (LeetCode), Luhn (Exercism).

## What's still rough

- No session persistence: refreshing the browser restarts the conversation. The `claude-agent-sdk` itself supports `session_id` / `resume`; not wired.
- No interrupt button. Once a turn starts, no way to cancel. SDK has `client.interrupt()`.
- No spend/turn caps (`max_budget_usd`, `max_turns` are unset on `ClaudeAgentOptions`).
- Tool restrictions in the system prompt; not enforced at the SDK level (we allow Read/Glob/Grep/Edit/Write/Bash). Trustworthy because of the prompt + bypass mode being a POC choice.
- Pre-existing project files in cwd cause friction (the system prompt has guidance, but it's still possible to hit Edit-without-Read errors). Easier if the user starts in a clean directory.

## Testing notes

- WebSocket smoke test pattern (used during development):
  ```python
  async with websockets.connect("ws://127.0.0.1:8000/ws") as ws:
      await ws.send(json.dumps({"type": "user_message", "text": "..."}))
      while True:
          ev = json.loads(await ws.recv())
          if ev.get("type") == "result": break
  ```
- Restart the server after `server.py` changes (system prompt, tool schema). Static UI files (`static/index.html`) are served fresh per request — just refresh the browser.

## Notable design decisions

- **Custom MCP tool over structured output via JSON schema**. The tool gives mechanical schema enforcement and a clean event channel; we suppress the stream events for our tool's content blocks server-side and emit a synthesized `options` event so the browser doesn't need to know about the underlying tool plumbing.
- **Plain-text user replies after options**, not `AskUserQuestion`-style multi-choice. Users type "A" / "B" / "the second one" / etc. — Claude parses intent. Selection becomes a normal user message; no special "kind" handling on the server.
- **Model-driven option ordering**, not server-side shuffle. If the server shuffled, Claude's `private_notes.best_index` would point to the wrong column. By having the model itself randomize, indices line up everywhere.
- **CLI-shaped wire vocabulary** (`stream-json`-ish events). When we want to add new event types or render differently, we know the existing CLI vocabulary and don't reinvent.
