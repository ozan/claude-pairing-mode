import json
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    StreamEvent,
    SystemMessage,
    TextBlock,
    ThinkingBlock,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
    create_sdk_mcp_server,
    tool,
)

STATIC_DIR = Path(__file__).parent / "static"

PROPOSE_TOOL_NAME = "propose_options"
MCP_SERVER_NAME = "proto_pair"
# Full name as Claude sees it after MCP registration:
FULL_TOOL_NAME = f"mcp__{MCP_SERVER_NAME}__{PROPOSE_TOOL_NAME}"

PROPOSE_INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "options": {
            "type": "array",
            "minItems": 2,
            "maxItems": 2,
            "items": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Very short label, 2-5 words. No punctuation.",
                    },
                    "body": {
                        "type": "string",
                        "description": (
                            "Brief markdown justification: 1-3 short sentences, ~40 words "
                            "max. Use fenced ```diff blocks for code changes. Save deeper "
                            "explanation for the post-selection feedback."
                        ),
                    },
                },
                "required": ["title", "body"],
            },
        },
        "private_notes": {
            "type": "object",
            "description": (
                "Hidden notes you keep for the followup turn. The user does NOT see this."
            ),
            "properties": {
                "best_index": {
                    "type": "integer",
                    "description": "0-based index of your honest best recommendation (0 or 1).",
                },
                "trap_flaw": {
                    "type": "string",
                    "description": "What is subtly wrong with the OTHER (distractor) option.",
                },
            },
            "required": ["best_index", "trap_flaw"],
        },
    },
    "required": ["options", "private_notes"],
}

SYSTEM_PROMPT = """\
You are an AI pair programmer designed to teach the user while you build the project together. Your
challenge is to balance productivity with pedagogy by picking opportune times to ask *didactic* questions.

A didactic question is one where you have confidence in the right answer and want to use the moment as a
teaching opportunity. This is in contrast to a clarifying question, where you genuinely need user preference
to proceed (no "wrong" answer). For clarifying questions, just assume sensible defaults inline (e.g., "I'll
go with Python") and proceed — don't stall on them. The user can redirect later.

When you identify a didactic moment, call the propose_options tool with TWO options:

  1. Your honest best recommendation.
  2. A plausible-looking distractor — tempting at first glance, but with a subtle flaw worth learning from.

Examples of good didactic decisions for a tic-tac-toe build:
  - Modeling the board state (1D list vs nested vs string)
  - Win-detection style (precomputed lines vs row/col/diag iteration)
  - Implementation correctness ("which of these two move() functions is correct?")

Randomize the order yourself: sometimes the best is index 0, sometimes index 1. The user shouldn't be
able to predict which is which. Set private_notes.best_index to 0 or 1 to record your recommendation,
and private_notes.trap_flaw to the subtle problem with the OTHER option.

KEEP OPTIONS SHORT. Each option body: 1-3 short sentences, ~40 words max. Title: 2-5 words. Don't hint
at which is best — present both even-handedly.

DIFF FORMAT (REQUIRED for code options): use fenced ```diff blocks containing UNIFIED DIFF format with
a hunk header. The hunk header is required so the UI can render line numbers. Example:

  ```diff
  +++ tic_tac_toe.py
  @@ -3,2 +3,5 @@
       board = [' '] * 9
  -    print(board)
  +    LINES = [(0,1,2),(3,4,5),(6,7,8),
  +             (0,3,6),(1,4,7),(2,5,8),
  +             (0,4,8),(2,4,6)]
  ```

Include a `+++ <filename>` header above the hunk so the UI picks the right syntax highlighter. For the
FIRST foundational decision when no file exists yet, treat the "before" file as empty: use
`@@ -0,0 +1,N @@` (where N is the line count) and prefix every line with `+`. Never use plain ```python
or ```js fences for option code — always ```diff with hunk headers.

After you call propose_options, the UI displays the two options as columns A and B. The user replies in
plain text — typically just "A" or "B", or a phrase like "the first one" or "let's go with B". Parse intent
freely. Then respond per role:

  - If they picked your best (private_notes.best_index): brief enthusiasm. Apply the change with Edit/Write
    and continue toward the next decision.
  - If they picked the distractor: be curious, not disparaging. Confidently state the subtle flaw (from
    private_notes.trap_flaw). Give them a chance to justify their choice, stick with it, or switch to the
    other option.

The question granularity should be such that the options are a few sentences or a 5-10 line diff. A
problem like tic-tac-toe might unfold across 10-20 such decisions.

Workflow for incremental code changes: after the first foundational decision is accepted, create the
starting file with Write. From then on, before proposing options for an incremental change, Read the
current file. Express each option as a unified diff in a ```diff fenced block. After the user picks,
apply that option's change with Edit before moving on.

File-path discipline: ALWAYS use plain relative paths (e.g. `tic_tac_toe.py`, not `/Users/.../...`).
The working directory is already correct. Before Write on a project file, check whether it exists
(Glob or `ls`). If it does, Read it first — then either Edit it or proceed with Write (now permitted
post-Read). Never Write a path you haven't verified is empty or have not Read.

Be succinct. Don't say the word "didactic" or discuss your role as a teacher. Act like a senior engineer
whose time is valuable but who occasionally slows down to share something worth learning.
"""


@tool(
    PROPOSE_TOOL_NAME,
    (
        "Propose exactly two options for the user to choose between at a didactic decision point. "
        "One option is your honest best recommendation; the other is a plausible-looking distractor "
        "with a subtle flaw to learn from. Randomize order. The user replies in plain text with their pick."
    ),
    PROPOSE_INPUT_SCHEMA,
)
async def propose_options(args):  # noqa: ARG001
    # Body is intentionally trivial. The SDK still routes the args through the
    # message stream, where the WS handler intercepts and reshapes them.
    return {"content": [{"type": "text", "text": "Options recorded; awaiting user selection."}]}


mcp_server = create_sdk_mcp_server(
    name=MCP_SERVER_NAME, tools=[propose_options]
)


app = FastAPI()


def _block_to_dict(block):
    if isinstance(block, TextBlock):
        return {"type": "text", "text": block.text}
    if isinstance(block, ToolUseBlock):
        return {"type": "tool_use", "id": block.id, "name": block.name, "input": block.input}
    if isinstance(block, ThinkingBlock):
        return {"type": "thinking", "thinking": block.thinking}
    if isinstance(block, ToolResultBlock):
        return {
            "type": "tool_result",
            "tool_use_id": block.tool_use_id,
            "content": block.content,
            "is_error": bool(block.is_error),
        }
    return None


class Connection:
    """Per-WebSocket conversation state."""

    def __init__(self, ws: WebSocket):
        self.ws = ws
        # tool_use_ids of our own propose_options calls — used to suppress the
        # synthetic "ok" tool_result when forwarding user messages to the browser.
        self.propose_tool_use_ids: set[str] = set()
        # Indices of stream content blocks to suppress in the current message
        self.suppressed_indices: set[int] = set()

    async def send(self, event):
        await self.ws.send_json(event)

    async def echo_user_input(self, text: str):
        await self.send(
            {
                "type": "user",
                "message": {
                    "role": "user",
                    "content": [{"type": "text", "text": text}],
                },
                "parent_tool_use_id": None,
            }
        )

    async def process_propose(self, block: ToolUseBlock):
        args = block.input or {}
        options = args.get("options") or []

        if not isinstance(options, list) or len(options) != 2:
            await self.send(
                {
                    "type": "error",
                    "message": f"propose_options expected exactly 2 options, got {len(options) if isinstance(options, list) else 'non-list'}",
                }
            )
            return

        # No server-side shuffle: the model orders options itself, and its
        # private_notes references the same indices the browser displays.
        public = [{"title": o.get("title", ""), "body": o.get("body", "")} for o in options]
        self.propose_tool_use_ids.add(block.id)
        await self.send(
            {
                "type": "options",
                "tool_use_id": block.id,
                "options": public,
            }
        )

    async def handle_sdk_msg(self, sdk_msg):
        if isinstance(sdk_msg, StreamEvent):
            await self._forward_stream_event(sdk_msg)
        elif isinstance(sdk_msg, AssistantMessage):
            await self._forward_assistant(sdk_msg)
        elif isinstance(sdk_msg, UserMessage):
            await self._forward_user(sdk_msg)
        elif isinstance(sdk_msg, ResultMessage):
            await self.send(
                {
                    "type": "result",
                    "subtype": sdk_msg.subtype,
                    "is_error": sdk_msg.is_error,
                    "duration_ms": sdk_msg.duration_ms,
                    "duration_api_ms": sdk_msg.duration_api_ms,
                    "num_turns": sdk_msg.num_turns,
                    "total_cost_usd": sdk_msg.total_cost_usd,
                    "result": sdk_msg.result,
                    "session_id": sdk_msg.session_id,
                }
            )
        elif isinstance(sdk_msg, SystemMessage):
            await self.send({"type": "system", "subtype": sdk_msg.subtype, "data": sdk_msg.data})

    async def _forward_stream_event(self, sdk_msg: StreamEvent):
        ev = sdk_msg.event or {}
        et = ev.get("type")

        if et == "message_start":
            self.suppressed_indices = set()
        elif et == "content_block_start":
            cb = ev.get("content_block") or {}
            if cb.get("type") == "tool_use" and cb.get("name") == FULL_TOOL_NAME:
                idx = ev.get("index")
                if idx is not None:
                    self.suppressed_indices.add(idx)
                return
        elif et in ("content_block_delta", "content_block_stop"):
            if ev.get("index") in self.suppressed_indices:
                return

        await self.send(
            {
                "type": "stream_event",
                "event": ev,
                "parent_tool_use_id": sdk_msg.parent_tool_use_id,
            }
        )

    async def _forward_assistant(self, msg: AssistantMessage):
        kept_blocks = []
        for block in msg.content:
            if isinstance(block, ToolUseBlock) and block.name == FULL_TOOL_NAME:
                await self.process_propose(block)
                continue
            d = _block_to_dict(block)
            if d is not None:
                kept_blocks.append(d)
        if kept_blocks:
            await self.send(
                {
                    "type": "assistant",
                    "message": {
                        "role": "assistant",
                        "model": msg.model,
                        "content": kept_blocks,
                    },
                    "parent_tool_use_id": msg.parent_tool_use_id,
                }
            )

    async def _forward_user(self, msg: UserMessage):
        if not isinstance(msg.content, list):
            return
        kept = []
        for block in msg.content:
            if (
                isinstance(block, ToolResultBlock)
                and block.tool_use_id in self.propose_tool_use_ids
            ):
                # Suppress the synthetic tool_result for our own tool
                continue
            d = _block_to_dict(block)
            if d is not None:
                kept.append(d)
        if kept:
            await self.send(
                {
                    "type": "user",
                    "message": {"role": "user", "content": kept},
                    "parent_tool_use_id": msg.parent_tool_use_id,
                }
            )

    def format_outgoing(self, msg: dict) -> str:
        return msg.get("text", "")

    def echo_text_for_browser(self, msg: dict) -> str | None:
        """Text to echo in the transcript for a user-initiated message; None to skip."""
        return msg.get("text", "") or None


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()

    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        cwd=str(Path.cwd()),
        include_partial_messages=True,
        system_prompt=SYSTEM_PROMPT,
        mcp_servers={MCP_SERVER_NAME: mcp_server},
        # Built-ins kept enabled so future code-mode steps can read files.
        # The system prompt forbids edits/bash; we'd lock those down too if needed.
        tools=["Read", "Glob", "Grep", "Edit", "Write", "Bash"],
        # Defaults: Opus, default effort, default (adaptive) thinking.
    )

    conn = Connection(ws)

    try:
        async with ClaudeSDKClient(options=options) as client:
            while True:
                raw = await ws.receive_text()
                msg = json.loads(raw)
                if msg.get("type") != "user_message":
                    continue

                # Echo to the transcript what the user did
                echo_text = conn.echo_text_for_browser(msg)
                if echo_text:
                    await conn.echo_user_input(echo_text)

                # Format the actual prompt sent to Claude
                outgoing = conn.format_outgoing(msg)

                try:
                    await client.query(outgoing)
                    async for sdk_msg in client.receive_response():
                        await conn.handle_sdk_msg(sdk_msg)
                except Exception as e:
                    await ws.send_json({"type": "error", "message": str(e)})
    except WebSocketDisconnect:
        return


app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
