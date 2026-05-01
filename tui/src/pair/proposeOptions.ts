// The didactic 2-option pair-programmer experiment's MCP tool definition,
// custom event type, and the handler that core's Session calls when the
// model invokes the tool. This file is the entire glue for plugging the
// experiment into core.

import { createSdkMcpServer, tool } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';
import { type CustomToolHandler, type ToolUseBlock } from '../core/types';

export const PROPOSE_TOOL_NAME = 'propose_options';
export const MCP_SERVER_NAME = 'proto_pair';
export const FULL_PROPOSE_TOOL_NAME =
  `mcp__${MCP_SERVER_NAME}__${PROPOSE_TOOL_NAME}`;


// Shape of the synthesized event the App renders as a 2-column option panel.
export type OptionsEvent = {
  kind: 'options';
  toolUseId: string;
  options: { title: string; body: string }[];
};


// MCP tool definition. Body is intentionally a no-op; the SDK still routes
// args through the message stream where our Session intercepts and reshapes
// them via the custom-tool handler below.
const proposeOptionsTool = tool(
  PROPOSE_TOOL_NAME,
  'Propose exactly two options for the user to choose between at a didactic decision point. ' +
    'One option is your honest best recommendation; the other is a plausible-looking distractor ' +
    'with a subtle flaw to learn from. Randomize order. The user replies in plain text with their pick.',
  {
    options: z
      .array(
        z.object({
          title: z.string().describe('Very short label, 2-5 words. No punctuation.'),
          body: z
            .string()
            .describe(
              'Brief markdown justification: 1-3 short sentences, ~40 words max. ' +
                'Use fenced ```diff blocks for code changes.',
            ),
        }),
      )
      .min(2)
      .max(2),
    private_notes: z.object({
      best_index: z
        .number()
        .int()
        .describe('0-based index of your honest best recommendation (0 or 1).'),
      trap_flaw: z
        .string()
        .describe('What is subtly wrong with the OTHER (distractor) option.'),
    }),
  },
  async () => ({
    content: [
      { type: 'text' as const, text: 'Options recorded; awaiting user selection.' },
    ],
  }),
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
  const args = (block.input ?? {}) as Record<string, unknown>;
  const options = args.options;
  if (
    Array.isArray(options) &&
    options.length === 2 &&
    options.every(
      (o) => o && typeof o === 'object' &&
        typeof (o as { title?: unknown }).title === 'string' &&
        typeof (o as { body?: unknown }).body === 'string',
    )
  ) {
    return {
      kind: 'options',
      toolUseId: block.id,
      options: (options as { title: string; body: string }[]).map((o) => ({
        title: o.title,
        body: o.body,
      })),
    };
  }
  // Malformed — return null so the id is claimed (SDK validation error
  // suppressed) but no event is emitted. The model retries.
  return null;
};
