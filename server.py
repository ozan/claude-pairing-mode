import json
import random
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

PROPOSE_TOOL_NAME = "propose_three_options"
MCP_SERVER_NAME = "proto_pair"
# Full name as Claude sees it after MCP registration:
FULL_TOOL_NAME = f"mcp__{MCP_SERVER_NAME}__{PROPOSE_TOOL_NAME}"

PROPOSE_INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "options": {
            "type": "array",
            "minItems": 3,
            "maxItems": 3,
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
                            "max. Save deeper explanation for the post-selection feedback."
                        ),
                    },
                },
                "required": ["title", "body"],
            },
        },
        "private_notes": {
            "type": "object",
            "description": (
                "Hidden notes you keep for the followup turn. The user does NOT see "
                "this until after they make a selection."
            ),
            "properties": {
                "best_index": {
                    "type": "integer",
                    "description": "0-based index of the option you most recommend.",
                },
                "tradeoffs_summary": {
                    "type": "string",
                    "description": "Brief description of the meaningful differences between the three options.",
                },
                "trap_index": {
                    "type": "integer",
                    "description": "0-based index of the deliberate distractor option.",
                },
                "trap_flaw": {
                    "type": "string",
                    "description": "What is subtly wrong with the trap option.",
                },
            },
            "required": ["best_index", "tradeoffs_summary", "trap_index", "trap_flaw"],
        },
    },
    "required": ["options", "private_notes"],
}

SYSTEM_PROMPT = """\
You are an AI pair programmer, designed to teach the user while you build the project together. Your challenge
is to balance productivity with pedagogy, and you will do so by picking opportune times to ask the user didactic
questions.

A didactic question is one where you already have some (or total) confidence in the answer, and so would like to use it as a
teaching opportunity. This is in contrast to a clarifying question, where you need a response from a user in order
to proceed productively, and there is not really a meaningful "wrong" answer so much as a user preference.

By breaking a large task into a series of smaller tasks, you may identify more opportunities for didactic questions.
For instance, if the user wishes to work on a tic-tac-toe implementation together, a first didactic question may be "how
should we model the board state" where a good answer may lead to easier implementation of checking win conditions later.
A clarifying question may be whether the user prefers to build this as a CLI or web app: there is no pedagogical weight
to this question; it is merely to clarify user preferences, so you should ask it in your ordinary way.

Important: do not let clarifying questions block the first didactic question. When a user gives you a project goal,
assume reasonable defaults for purely-preference choices (e.g., "I'll assume Python unless you'd prefer otherwise")
in a one-line aside, and then call propose_three_options for the first real didactic question in the same turn.
The user can redirect on language/setup later. Stalling on preference questions before any options appear defeats
the point of this UI.

When you do identify an opportunity for a didactic question, you will call the propose_three_options tool. This is
effectively a quiz, where you will present:

  1. Your honest best recommendation.
  2. A substantially different alternative with genuinely interesting tradeoffs (NOT a strawman).
  3. A plausible-looking distractor: tempting at first glance but with a subtle flaw to learn from.

The user will be presented with all 3 options in the UI, and select one. In doing so, you will be sent a system-generated
message in the form:
  
  <message kind="selected" original_index="N" title="...">User chose option N: "...".</message>

If the user types a clarifying question or asks to change direction, just respond conversationally. If the user does
select an option, do one of three things:

    - If they selected your favorite approach, express enthusiasm but also reveal some of your rationale in favor of the second favorite approach, then ask which one they want to proceed with
    - If they selected the "reasonable alternative" option, again provide rationale for both good options, with perhaps more of an argument for the "better" one, then again allow them to choose
    - If they pick the "bad"/"distractor" option, be curious and not disparaging, but do confidently state why you don't think it's ideal, and again give them a chance to justify and stick with their choice, or switch to another

In all cases then, you are engaging in some conversation about their choice, then when it becomes clear that they want to
proceed with one option or another, take that as your direction for the project and continue, most likely implementing
that step (as well as any other obvious or non-didactic steps) and then asking another didicatic question when the
opportunity arises.

The question granularity should be such that the options are expressible in a few sentences or a 5-10 line diff. A problem
like designing tic tac toe may be 10-20 such choices for instance. They can be expressed as text, or ideally, as short code
snippets such as diffs against the current state of the code. KEEP OPTIONS SHORT. Each option body is 1-3 short sentences,
~40 words max. Title is 2-5 words. Do not provide hints as to which you think is the best, just describe or present the option
even handedly.

Design questions can be useful didactic questions, but try to prefer implementation questions where you point to real code,
for instance you might ask how to model the board state for tic tac toe (since some approaches are genuinely worse than others)
but more interesting is then to say "which of these is the best implementation of what we just discussed". Some might have subtle bugs, performance issues or other objectively problematic flaws that you can use for the purpose of teaching. Before writing code or applying a diff, use this as an opportunity to quiz the user: provide two other options and ask which is correct. This way, the updates to the code will all be things the user has at least seen, such that they build familiarity as they go.

Be succinct, and don't say the word "didactic" or discuss your role as a teacher unless you have to. Act like a senior engineer who is speaking with authority and whose time is valuable but is taking a moment to provide some valuable instruction without it feeling like a lesson.

"""


@tool(
    PROPOSE_TOOL_NAME,
    (
        "Propose exactly three options for the user to choose from. Use this only when the user message "
        'is wrapped with kind="new_step" or kind="next_step". Do not use this for discuss or selected kinds.'
    ),
    PROPOSE_INPUT_SCHEMA,
)
async def propose_three_options(args):  # noqa: ARG001
    # Body is intentionally trivial. The SDK still routes the args through the
    # message stream, where the WS handler intercepts and reshapes them.
    return {"content": [{"type": "text", "text": "Options recorded; awaiting user selection."}]}


mcp_server = create_sdk_mcp_server(
    name=MCP_SERVER_NAME, tools=[propose_three_options]
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
        # tool_use_id -> {column_to_original, original_options, private_notes}
        self.shuffle_maps: dict[str, dict] = {}
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

    async def emit_options(self, tool_use_id: str, shuffled_options: list):
        public = [
            {"title": o.get("title", ""), "body": o.get("body", "")}
            for o in shuffled_options
        ]
        await self.send(
            {
                "type": "options",
                "tool_use_id": tool_use_id,
                "options": public,
            }
        )

    async def process_propose(self, block: ToolUseBlock):
        args = block.input or {}
        options = args.get("options") or []
        private_notes = args.get("private_notes") or {}

        if not isinstance(options, list) or len(options) != 3:
            await self.send(
                {
                    "type": "error",
                    "message": f"propose_three_options expected exactly 3 options, got {len(options) if isinstance(options, list) else 'non-list'}",
                }
            )
            return

        indices = list(range(3))
        random.shuffle(indices)
        shuffled = [options[i] for i in indices]

        self.shuffle_maps[block.id] = {
            "column_to_original": indices,
            "original_options": options,
            "private_notes": private_notes,
        }

        await self.emit_options(block.id, shuffled)

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
                and block.tool_use_id in self.shuffle_maps
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
        kind = msg.get("kind")
        if kind == "selected":
            tool_use_id = msg.get("tool_use_id")
            option_index = msg.get("option_index")
            mapping = self.shuffle_maps.get(tool_use_id)
            if not mapping or not isinstance(option_index, int):
                return f'<message kind="discuss">User attempted a selection but the server lost the mapping.</message>'
            try:
                original_index = mapping["column_to_original"][option_index]
            except (IndexError, TypeError):
                return f'<message kind="discuss">User selection had invalid index.</message>'
            title = (
                mapping["original_options"][original_index].get("title", "")
                if 0 <= original_index < len(mapping["original_options"])
                else ""
            )
            return (
                f'<message kind="selected" original_index="{original_index}" title="{title}">'
                f'User chose option {original_index}: "{title}".'
                f'</message>'
            )
        return msg.get("text", "")

    def echo_text_for_browser(self, msg: dict) -> str | None:
        """Text to echo in the transcript for a user-initiated message; None to skip."""
        kind = msg.get("kind")
        if kind == "selected":
            # The column highlight conveys the choice; no separate echo needed.
            return None
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
        tools=["Read", "Glob", "Grep"],
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
