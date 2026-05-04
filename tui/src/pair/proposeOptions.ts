// The didactic 2-option pair-programmer experiment's MCP tool definition,
// custom event type, and the handler that core's Session calls when the
// model invokes the tool. This file is the entire glue for plugging the
// experiment into core.
//
// The tool's name, description, and input schema live in the shared JSON
// file at the repo root (../../../propose_options_tool_schema.json) so the
// Python eval and this TS TUI register the exact same contract with the
// model. The schema is FLAT (six top-level fields, no nesting): see that
// file for field definitions, and 006-initial transcripts for the prior
// nested-schema breakage that motivated the flat shape.

import { createSdkMcpServer, tool } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';
import { type CustomToolHandler, type ToolUseBlock } from '../core/types';
import schemaJson from '../../../propose_options_tool_schema.json' with { type: 'json' };


interface ToolSchema {
  mcp_server_name: string;
  tool_name: string;
  description: string;
  input_schema: {
    type: 'object';
    properties: Record<string, { type: 'string'; description: string; enum?: string[] }>;
    required: string[];
  };
}
const SCHEMA = schemaJson as ToolSchema;

export const PROPOSE_TOOL_NAME = SCHEMA.tool_name;
export const MCP_SERVER_NAME = SCHEMA.mcp_server_name;
export const FULL_PROPOSE_TOOL_NAME =
  `mcp__${MCP_SERVER_NAME}__${PROPOSE_TOOL_NAME}`;


// Shape of the synthesized event the App renders as a 2-column option panel.
export type OptionsEvent = {
  kind: 'options';
  toolUseId: string;
  options: { title: string; body: string }[];
  /**
   * Model's private annotations. Not rendered in the UI — preserved on the
   * event so the eval/transcript layer can score "did the user pick the
   * model's preferred option?" Absent if validation failed.
   */
  privateNotes?: { bestIndex?: number; rationale?: string };
};


// Build a Zod raw shape from the shared JSON schema. Supports the limited
// subset our tool uses: string + string-enum, both with descriptions.
const zodShape = Object.fromEntries(
  Object.entries(SCHEMA.input_schema.properties).map(([key, prop]) => {
    const base = prop.enum
      ? z.enum(prop.enum as [string, ...string[]])
      : z.string();
    return [key, base.describe(prop.description)];
  }),
);


const proposeOptionsTool = tool(
  PROPOSE_TOOL_NAME,
  SCHEMA.description,
  zodShape,
  async () => ({
    content: [
      { type: 'text' as const, text: 'Options recorded; awaiting user selection.' },
    ],
  }),
  // alwaysLoad: true makes the tool eager (in main tools list, no
  // ToolSearch dance). With a deferred tool (alwaysLoad omitted), Sonnet
  // sometimes skips ToolSearch and calls directly; the SDK then rejects
  // with "No such tool available" because the schema isn't loaded.
  // alwaysLoad eliminates that protocol gap. Combined with the flat
  // all-string schema this should yield reliable dispatch.
  { alwaysLoad: true },
);


export const pairMcpServer = createSdkMcpServer({
  name: MCP_SERVER_NAME,
  version: '0.1.0',
  tools: [proposeOptionsTool],
});


/**
 * Custom tool handler core's Session invokes when the model calls
 * propose_options. Validates the args; on success returns the synthesized
 * `options` event, on failure returns null (which still claims the
 * tool_use_id so the SDK's validation error tool_result is suppressed —
 * the model can retry without leaking errors into the transcript).
 */
export const proposeOptionsHandler: CustomToolHandler<OptionsEvent> = (block: ToolUseBlock) => {
  const a = (block.input ?? {}) as Record<string, unknown>;
  const aT = a.option_a_title;
  const aB = a.option_a_body;
  const bT = a.option_b_title;
  const bB = a.option_b_body;
  if (
    typeof aT === 'string' &&
    typeof aB === 'string' &&
    typeof bT === 'string' &&
    typeof bB === 'string'
  ) {
    const bestLetter = a.best_letter;
    const bestIndex = bestLetter === 'A' ? 0 : bestLetter === 'B' ? 1 : undefined;
    const rationale = typeof a.rationale === 'string' ? a.rationale : undefined;
    return {
      kind: 'options',
      toolUseId: block.id,
      options: [
        { title: aT, body: aB },
        { title: bT, body: bB },
      ],
      privateNotes: { bestIndex, rationale },
    };
  }
  // Malformed — return null so the id is claimed (SDK validation error
  // suppressed) but no event is emitted. The model retries.
  return null;
};
