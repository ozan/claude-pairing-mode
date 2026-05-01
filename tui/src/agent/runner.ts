// Long-running session wrapper around @anthropic-ai/claude-agent-sdk's query().
// Replaces the per-turn `runTurn(prompt)` model with a single Session that
// owns one Query for the whole app lifetime — so conversation history
// persists across user turns (the model remembers what it just said).
//
// Pattern: query() accepts an AsyncIterable<SDKUserMessage>. We control that
// iterable via an unbounded queue. Submitting a turn pushes a user message
// into the queue; consuming the Query's messages yields events that we
// translate to our high-level event vocabulary.
//
// Event vocabulary (kept stable from the Python tui/agent_runner.py):
//   { kind: "text_delta", text }
//   { kind: "text_block_done" }
//   { kind: "tool_use_start", id, name, input }
//   { kind: "tool_use_done", id, input }
//   { kind: "tool_result", toolUseId, name, text, isError }
//   { kind: "options", toolUseId, options: { title, body }[] }
//   { kind: "result", durationMs, totalCostUsd, numTurns }
//   { kind: "error", message }

import {
  createSdkMcpServer,
  query,
  tool,
  type SDKUserMessage,
} from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';
import { SYSTEM_PROMPT } from './systemPrompt';

const PROPOSE_TOOL_NAME = 'propose_options';
const MCP_SERVER_NAME = 'proto_pair';
const FULL_TOOL_NAME = `mcp__${MCP_SERVER_NAME}__${PROPOSE_TOOL_NAME}`;

// Internal SDK tools that shouldn't appear in the user-facing transcript.
// The Node SDK fires `ToolSearch` to resolve deferred MCP tools at startup —
// pure plumbing, not real activity.
const HIDDEN_TOOL_NAMES = new Set(['ToolSearch']);

const proposeOptions = tool(
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

const mcpServer = createSdkMcpServer({
  name: MCP_SERVER_NAME,
  version: '0.1.0',
  tools: [proposeOptions],
});

export type AgentEvent =
  | { kind: 'text_delta'; text: string }
  | { kind: 'text_block_done' }
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
      kind: 'options';
      toolUseId: string;
      options: { title: string; body: string }[];
    }
  | { kind: 'result'; durationMs: number; totalCostUsd: number; numTurns: number }
  | { kind: 'error'; message: string };


/** Async queue with a `push` method that satisfies AsyncIterable<SDKUserMessage>. */
class UserMessageQueue implements AsyncIterable<SDKUserMessage> {
  private buffered: SDKUserMessage[] = [];
  private waiting: ((m: SDKUserMessage) => void)[] = [];
  private closed = false;

  push(msg: SDKUserMessage): void {
    if (this.closed) return;
    const w = this.waiting.shift();
    if (w) w(msg);
    else this.buffered.push(msg);
  }

  close(): void {
    this.closed = true;
    // Wake up any waiters with a no-op iteration end. The async iterator
    // checks `closed` after wake.
    for (const w of this.waiting) w(null as unknown as SDKUserMessage);
    this.waiting = [];
  }

  async *[Symbol.asyncIterator](): AsyncIterator<SDKUserMessage> {
    while (!this.closed) {
      if (this.buffered.length > 0) {
        yield this.buffered.shift()!;
        continue;
      }
      const msg = await new Promise<SDKUserMessage>((resolve) => {
        this.waiting.push(resolve);
      });
      if (this.closed) break;
      yield msg;
    }
  }
}


export class Session {
  private queue = new UserMessageQueue();
  private listener: ((ev: AgentEvent) => void) | null = null;
  private consumePromise: Promise<void> | null = null;
  private propseIds = new Set<string>();
  private hiddenToolIds = new Set<string>();
  private suppressedIndices = new Set<number>();
  private toolNames = new Map<string, string>();
  private turnStartedAt = Date.now();

  /** Begin consuming the long-running Query. Call once at app start. */
  start(): void {
    if (this.consumePromise) return;
    const q = query({
      prompt: this.queue,
      options: {
        mcpServers: { [MCP_SERVER_NAME]: mcpServer },
        systemPrompt: SYSTEM_PROMPT,
        permissionMode: 'bypassPermissions',
        allowedTools: ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash'],
        includePartialMessages: true,
      },
    });

    this.consumePromise = (async () => {
      try {
        for await (const msg of q) {
          this.translate(msg);
        }
      } catch (e) {
        const err = e as Error;
        this.emit({ kind: 'error', message: `${err.name}: ${err.message}` });
      }
    })();
  }

  /** Subscribe to events. Only one listener is supported. */
  onEvent(handler: (ev: AgentEvent) => void): void {
    this.listener = handler;
  }

  /** Send a user prompt; events flow back via the listener. */
  send(text: string): void {
    this.turnStartedAt = Date.now();
    this.suppressedIndices.clear();
    this.queue.push({
      type: 'user',
      message: { role: 'user', content: text },
      parent_tool_use_id: null,
    });
  }

  close(): void {
    this.queue.close();
  }

  private emit(ev: AgentEvent): void {
    this.listener?.(ev);
  }

  private translate(msg: unknown): void {
    const m = msg as { type?: string };
    const type = m.type;

    if (type === 'stream_event') {
      const ev = (msg as { event: { type: string; index?: number; content_block?: { type: string; name?: string; id?: string }; delta?: { type: string; text?: string } } }).event;
      const et = ev.type;

      if (et === 'message_start') {
        this.suppressedIndices.clear();
        return;
      }
      if (et === 'content_block_start') {
        const cb = ev.content_block!;
        const idx = ev.index;
        if (cb.type === 'tool_use' && cb.name === FULL_TOOL_NAME) {
          if (idx !== undefined) this.suppressedIndices.add(idx);
          return;
        }
        if (cb.type === 'text') return;
        if (cb.type === 'tool_use') {
          const toolName = cb.name ?? '';
          this.toolNames.set(cb.id ?? '', toolName);
          if (HIDDEN_TOOL_NAMES.has(toolName)) {
            this.hiddenToolIds.add(cb.id ?? '');
            return;
          }
          this.emit({
            kind: 'tool_use_start',
            id: cb.id ?? '',
            name: toolName,
            input: {},
          });
          return;
        }
        return;
      }
      if (et === 'content_block_delta') {
        if (ev.index !== undefined && this.suppressedIndices.has(ev.index)) return;
        const d = ev.delta!;
        if (d.type === 'text_delta') {
          this.emit({ kind: 'text_delta', text: d.text ?? '' });
          return;
        }
      }
      if (et === 'content_block_stop') {
        if (ev.index !== undefined && this.suppressedIndices.has(ev.index)) return;
        this.emit({ kind: 'text_block_done' });
      }
      return;
    }

    if (type === 'assistant') {
      const am = (msg as { message: { content: Array<{ type: string; id?: string; name?: string; input?: unknown }> } }).message;
      for (const block of am.content) {
        if (block.type === 'tool_use' && block.name === FULL_TOOL_NAME) {
          // Always claim the tool_use_id so the resulting tool_result
          // (whether success-stub or zod validation error) is suppressed —
          // a failed call gets retried by the model and shouldn't leak a
          // garbage `● Tool({})` MCP-error pill into the transcript.
          this.propseIds.add(block.id ?? '');

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
            this.emit({
              kind: 'options',
              toolUseId: block.id ?? '',
              options: (options as { title: string; body: string }[]).map((o) => ({
                title: o.title,
                body: o.body,
              })),
            });
          }
          // Else: malformed args. SDK will surface an MCP validation error
          // tool_result; we suppress it via propseIds and let the model
          // retry. No user-facing noise.
          continue;
        }
        if (block.type === 'tool_use') {
          const toolName = block.name ?? '';
          this.toolNames.set(block.id ?? '', toolName);
          if (HIDDEN_TOOL_NAMES.has(toolName)) {
            this.hiddenToolIds.add(block.id ?? '');
            continue;
          }
          this.emit({
            kind: 'tool_use_done',
            id: block.id ?? '',
            input: block.input ?? {},
          });
        }
      }
      return;
    }

    if (type === 'user') {
      const um = (msg as { message: { content: Array<{ type: string; tool_use_id?: string; content?: unknown; is_error?: boolean }> } }).message;
      if (!Array.isArray(um.content)) return;
      for (const block of um.content) {
        if (block.type !== 'tool_result') continue;
        const tuId = block.tool_use_id ?? '';
        if (this.propseIds.has(tuId)) continue;
        if (this.hiddenToolIds.has(tuId)) continue;
        let text = '';
        if (typeof block.content === 'string') text = block.content;
        else if (Array.isArray(block.content)) {
          text = (block.content as Array<{ text?: string }>)
            .map((c) => c.text ?? '')
            .join('');
        }
        this.emit({
          kind: 'tool_result',
          toolUseId: tuId,
          name: this.toolNames.get(tuId) ?? 'Tool',
          text,
          isError: Boolean(block.is_error),
        });
      }
      return;
    }

    if (type === 'result') {
      const r = msg as { duration_ms?: number; total_cost_usd?: number; num_turns?: number };
      this.emit({
        kind: 'result',
        durationMs: r.duration_ms ?? Date.now() - this.turnStartedAt,
        totalCostUsd: r.total_cost_usd ?? 0,
        numTurns: r.num_turns ?? 0,
      });
      return;
    }
  }
}
