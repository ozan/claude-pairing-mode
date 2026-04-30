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
)

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI()


def _block_to_dict(block):
    if isinstance(block, TextBlock):
        return {"type": "text", "text": block.text}
    if isinstance(block, ToolUseBlock):
        return {
            "type": "tool_use",
            "id": block.id,
            "name": block.name,
            "input": block.input,
        }
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


def serialize(sdk_msg):
    """Translate SDK messages to CLI-compatible stream-json events."""
    if isinstance(sdk_msg, StreamEvent):
        yield {
            "type": "stream_event",
            "event": sdk_msg.event,
            "parent_tool_use_id": sdk_msg.parent_tool_use_id,
        }
    elif isinstance(sdk_msg, AssistantMessage):
        content = [b for b in (_block_to_dict(b) for b in sdk_msg.content) if b]
        yield {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "model": sdk_msg.model,
                "content": content,
            },
            "parent_tool_use_id": sdk_msg.parent_tool_use_id,
        }
    elif isinstance(sdk_msg, UserMessage):
        if isinstance(sdk_msg.content, list):
            content = [b for b in (_block_to_dict(b) for b in sdk_msg.content) if b]
        else:
            content = [{"type": "text", "text": sdk_msg.content}]
        yield {
            "type": "user",
            "message": {"role": "user", "content": content},
            "parent_tool_use_id": sdk_msg.parent_tool_use_id,
        }
    elif isinstance(sdk_msg, ResultMessage):
        yield {
            "type": "result",
            "subtype": sdk_msg.subtype,
            "is_error": sdk_msg.is_error,
            "duration_ms": sdk_msg.duration_ms,
            "duration_api_ms": sdk_msg.duration_api_ms,
            "num_turns": sdk_msg.num_turns,
            "total_cost_usd": sdk_msg.total_cost_usd,
            "result": sdk_msg.result,
            "usage": sdk_msg.usage,
            "session_id": sdk_msg.session_id,
        }
    elif isinstance(sdk_msg, SystemMessage):
        yield {
            "type": "system",
            "subtype": sdk_msg.subtype,
            "data": sdk_msg.data,
        }


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()

    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        cwd=str(Path.cwd()),
        include_partial_messages=True,
    )

    try:
        async with ClaudeSDKClient(options=options) as client:
            while True:
                raw = await ws.receive_text()
                msg = json.loads(raw)
                if msg.get("type") != "user_message":
                    continue
                text = msg.get("text", "")
                if not text.strip():
                    continue

                await ws.send_json(
                    {
                        "type": "user",
                        "message": {
                            "role": "user",
                            "content": [{"type": "text", "text": text}],
                        },
                        "parent_tool_use_id": None,
                    }
                )

                try:
                    await client.query(text)
                    async for sdk_msg in client.receive_response():
                        for event in serialize(sdk_msg):
                            await ws.send_json(event)
                except Exception as e:
                    await ws.send_json({"type": "error", "message": str(e)})
    except WebSocketDisconnect:
        return


app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
