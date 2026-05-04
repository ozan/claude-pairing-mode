// Core event vocabulary — what a generic chat session emits. Experiments
// extend this with their own event kinds (e.g. pair/'s `options` event).

export type CoreAgentEvent =
  | { kind: 'text_delta'; text: string }
  | { kind: 'text_block_done' }
  | { kind: 'thinking_block_done'; text: string }
  | { kind: 'tool_use_start'; id: string; name: string; input: unknown }
  | { kind: 'tool_use_done'; id: string; input: unknown }
  | {
      kind: 'tool_result';
      toolUseId: string;
      name: string;
      text: string;
      isError: boolean;
    }
  | {
      kind: 'result';
      durationMs: number;
      totalCostUsd: number;
      numTurns: number;
    }
  | { kind: 'error'; message: string };

/** A tool_use block as the assistant emits it. */
export type ToolUseBlock = {
  id: string;
  name: string;
  input: unknown;
};

/**
 * Handler for a custom tool — invoked when an assistant tool_use block
 * matches `toolName`. Return:
 *   - a custom event (any object with a `kind`) to emit instead of the
 *     default `tool_use_done`. The tool's `tool_result` will be suppressed.
 *   - `null` to suppress everything for this tool (no event, no result).
 *   - `undefined` to fall through to default behavior.
 */
export type CustomToolHandler<E> = (block: ToolUseBlock) => E | null | undefined;
