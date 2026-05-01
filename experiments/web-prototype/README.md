# web-prototype (stashed)

The original Python + FastAPI + WebSocket front-end for the didactic 2-option
pair-programming experiment. Stashed here on 2026-05-02 in favour of the
TS/Bun/Ink TUI in `tui/` — the JS path is now the active surface, and
keeping two front-ends in sync was costing more than it was worth.

This still works; we just don't iterate on it.

## Run it

```bash
cd experiments/web-prototype
uv sync                # first time only — recreates the .venv
uv run uvicorn server:app --host 127.0.0.1 --port 8000 --log-level warning
```

Open <http://127.0.0.1:8000>. WebSocket-driven; do not pass `--reload` (it kills
the live WebSocket mid-turn). After editing `server.py`, kill and restart
manually.

## What's in here

```
server.py         FastAPI app + /ws WebSocket endpoint. Defines SYSTEM_PROMPT
                  and an in-process MCP tool propose_options
                  (claude-agent-sdk's create_sdk_mcp_server / @tool).
                  Per-WebSocket Connection class scrubs private_notes from
                  the stream and emits a synthesized {type: "options"} event
                  to clients. Wire format follows Claude Code's stream-json:
                  stream_event / assistant / user / result / system, plus
                  custom options / error.

static/index.html Single-page UI. WebSocket client. Two-column option cards;
                  user types A/B/letters/phrases (no click selection).
                  marked.js + highlight.js for streaming markdown.
                  Custom diff rendering matched to CC's Edit-tool output:
                  ADD bg rgb(2,40,0)/fg rgb(80,200,80), DEL bg rgb(61,1,0)/
                  fg rgb(220,90,90), hunk fg rgb(102,217,239); per-line hljs
                  via :where() rules so token colours override the line fg
                  while the diff line bg is preserved.
                  Tool-call pills, expandable tool-result summaries, rotating
                  "Pondering…" loader.

pyproject.toml + uv.lock   Python project (claude-agent-sdk, fastapi,
                            uvicorn[standard]). Python 3.14.
```

## Why we paused

The active surface is `tui/` (Bun + React 19 + Ink + the official
`@anthropic-ai/claude-agent-sdk`). We pivoted there because that's the same
stack the real `claude` CLI uses (verified by inspecting CC's compiled
binary), so we get pixel-near-parity essentially for free. The web prototype
explored the same UX paradigm but in a different surface and was harder to
keep visually consistent with what users see in CC.

If you ever want to come back to the web (e.g. to demo without Bun, or to
embed in a webapp), it's all here.
