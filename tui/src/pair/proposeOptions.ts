// The didactic 2-option pair-programmer experiment's MCP tool definition,
// custom event type, and the handler that core's Session calls when the
// model invokes the tool. This file is the entire glue for plugging the
// experiment into core.

import { createSdkMcpServer, tool } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';
import { type CustomToolHandler, type ToolUseBlock } from '../core/types';

export const PROPOSE_TOOL_NAME = 'propose_options';
export const MCP_SERVER_NAME = 'pairing';
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


// FLAT SCHEMA. The original schema had nested `options: Array<{title,
// body}>` + `private_notes: {best_index, rationale}` shape. Sonnet/Opus
// frequently serialized those nested fields as JSON-encoded strings,
// which the SDK pre-rejected with "No such tool available" — leaking
// the error into Sonnet's conversation history and breaking ~83% of
// runs in 006-initial. Verified via diag-minimal-mcp.ts that flat-arg
// MCP tools dispatch cleanly. The handler reconstructs the OptionsEvent
// from the six flat fields.
const proposeOptionsTool = tool(
  PROPOSE_TOOL_NAME,
  'Propose exactly two options for the user to choose between at a didactic decision point. ' +
    'Option A is what you would do if the user just asked, and option B is a plausible-looking ' +
    'alternative presented for educational purposes (or vice versa — vary which letter is your ' +
    'preference). Pass each field as a plain string or integer; do not JSON-encode them.',
  {
    option_a_title: z.string().describe('Short label for option A, 2-5 words. No punctuation.'),
    option_a_body: z
      .string()
      .describe(
        'Markdown justification for option A. Ideally 1-3 sentences. For code options, use a fenced ' +
          '```diff block with a `+++ filename` header and a `@@ -OLD,_ +NEW,_ @@` hunk header.',
      ),
    option_b_title: z.string().describe('Short label for option B, 2-5 words. No punctuation.'),
    option_b_body: z
      .string()
      .describe(
        'Markdown justification for option B. Same formatting rules as option_a_body.',
      ),
    best_letter: z
      .enum(['A', 'B'])
      .describe('"A" if option A is your honest best recommendation, "B" if option B is.'),
    rationale: z
      .string()
      .describe(
        'Your reasoning for and against the preferred option. Hidden from the user; used by ' +
          'the eval/transcript layer to score whether the user picked correctly.',
      ),
  },
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
