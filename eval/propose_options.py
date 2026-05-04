"""Python definition of the propose_options MCP tool.

The model-visible contract (name, description, input schema) lives in
../propose_options_tool_schema.json at the repo root and is shared with
tui/src/pair/proposeOptions.ts. The handler here is a thin stub: it just
acknowledges the call. The eval runner extracts the model's args (option
titles/bodies, best_letter, rationale) directly from the tool_use block,
not from anything the handler returns.
"""

import json
from pathlib import Path

from claude_agent_sdk import tool


SCHEMA_PATH = Path(__file__).parent.parent / "propose_options_tool_schema.json"
SCHEMA = json.loads(SCHEMA_PATH.read_text())

MCP_SERVER_NAME = SCHEMA["mcp_server_name"]
TOOL_NAME = SCHEMA["tool_name"]
FULL_TOOL_NAME = f"mcp__{MCP_SERVER_NAME}__{TOOL_NAME}"


@tool(TOOL_NAME, SCHEMA["description"], SCHEMA["input_schema"])
async def propose_options(args):
    return {
        "content": [
            {"type": "text", "text": "Options recorded; awaiting user selection."}
        ]
    }
