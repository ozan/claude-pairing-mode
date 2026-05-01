// Long-running session wrapper around @anthropic-ai/claude-agent-sdk's query().
//
// All turns share one Query so conversation history persists. Submitting a
// turn pushes a user message into a queue that the SDK consumes as
// AsyncIterable<SDKUserMessage>; consuming the Query's messages yields raw
// SDK objects that this class translates into CoreAgentEvents (plus any
// experiment-specific events emitted by registered customToolHandlers).
//
// Generic over the extra-event type `E` so experiments can extend the event
// vocabulary without modifying core. e.g. pair/ uses `Session<OptionsEvent>`.

import {
  query,
  type McpServerConfig,
  type SDKUserMessage,
} from '@anthropic-ai/claude-agent-sdk';
import {
  type CoreAgentEvent,
  type CustomToolHandler,
  type ToolUseBlock,
} from './types';


// Internal SDK tools that shouldn't appear in the user-facing transcript.
// The Node SDK fires `ToolSearch` to resolve deferred MCP tools — pure
// plumbing, not real activity.
const HIDDEN_TOOL_NAMES = new Set(['ToolSearch']);


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


export type SessionOptions<E> = {
  systemPrompt: string;
  mcpServers?: Record<string, McpServerConfig>;
  allowedTools?: string[];
  /**
   * Map of tool name (full SDK name like `mcp__server__tool_name`) → handler.
   * When the assistant calls a tool whose name is a key here, the handler
   * gets the tool_use block and decides what (if anything) to emit. Stream
   * events for these tools' content blocks are also suppressed (no
   * tool_use_start), and their tool_results are swallowed.
   */
  customToolHandlers?: Record<string, CustomToolHandler<E>>;
};


export class Session<E = never> {
  private queue = new UserMessageQueue();
  private listener: ((ev: CoreAgentEvent | E) => void) | null = null;
  private consumePromise: Promise<void> | null = null;

  // Tool ids whose tool_result we should suppress (because a custom handler
  // is owning the rendering for that tool).
  private claimedToolIds = new Set<string>();
  // Stream-event indices for tool_use blocks we're not surfacing as
  // tool_use_start (so their content_block_delta / content_block_stop also
  // get filtered).
  private suppressedIndices = new Set<number>();
  // Tool ids whose name we've recorded — used to populate the `name` field
  // on tool_result events.
  private toolNames = new Map<string, string>();
  // Ids of tools registered as hidden (ToolSearch + any custom-handled).
  private hiddenToolIds = new Set<string>();

  private turnStartedAt = Date.now();

  constructor(private opts: SessionOptions<E>) {}

  /** Begin consuming the long-running Query. Call once at app start. */
  start(): void {
    if (this.consumePromise) return;
    const q = query({
      prompt: this.queue,
      options: {
        mcpServers: this.opts.mcpServers ?? {},
        systemPrompt: this.opts.systemPrompt,
        permissionMode: 'bypassPermissions',
        allowedTools: this.opts.allowedTools ?? ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash'],
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
        this.emit({ kind: 'error', message: `${err.name}: ${err.message}` } as CoreAgentEvent);
      }
    })();
  }

  /** Subscribe to events. Only one listener supported. */
  onEvent(handler: (ev: CoreAgentEvent | E) => void): void {
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

  private emit(ev: CoreAgentEvent | E): void {
    this.listener?.(ev);
  }

  private isCustomTool(name: string): boolean {
    return this.opts.customToolHandlers
      ? Object.prototype.hasOwnProperty.call(this.opts.customToolHandlers, name)
      : false;
  }

  /**
   * Map a single raw SDK message to high-level event(s) via the listener.
   * Public so tests can drive translation with synthetic SDK messages —
   * runtime callers should not invoke this directly.
   */
  translate(msg: unknown): void {
    const m = msg as { type?: string };
    const type = m.type;

    if (type === 'stream_event') {
      const ev = (msg as {
        event: {
          type: string;
          index?: number;
          content_block?: { type: string; name?: string; id?: string };
          delta?: { type: string; text?: string };
        };
      }).event;
      const et = ev.type;

      if (et === 'message_start') {
        this.suppressedIndices.clear();
        return;
      }
      if (et === 'content_block_start') {
        const cb = ev.content_block!;
        const idx = ev.index;
        if (cb.type === 'tool_use') {
          const toolName = cb.name ?? '';
          this.toolNames.set(cb.id ?? '', toolName);
          if (HIDDEN_TOOL_NAMES.has(toolName) || this.isCustomTool(toolName)) {
            this.hiddenToolIds.add(cb.id ?? '');
            if (idx !== undefined) this.suppressedIndices.add(idx);
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
        if (cb.type === 'text') return;
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
      const am = (msg as {
        message: { content: Array<{ type: string; id?: string; name?: string; input?: unknown }> };
      }).message;
      for (const block of am.content) {
        if (block.type !== 'tool_use') continue;
        const toolName = block.name ?? '';
        const toolId = block.id ?? '';
        this.toolNames.set(toolId, toolName);

        const customHandler = this.opts.customToolHandlers?.[toolName];
        if (customHandler) {
          // Always claim the id so the SDK's tool_result (success-stub or
          // validation error) is suppressed — regardless of whether the
          // handler emits an event.
          this.claimedToolIds.add(toolId);
          const result = customHandler(block as ToolUseBlock);
          if (result !== null && result !== undefined) {
            this.emit(result);
          }
          continue;
        }
        if (HIDDEN_TOOL_NAMES.has(toolName)) {
          this.hiddenToolIds.add(toolId);
          continue;
        }
        this.emit({
          kind: 'tool_use_done',
          id: toolId,
          input: block.input ?? {},
        });
      }
      return;
    }

    if (type === 'user') {
      const um = (msg as {
        message: { content: Array<{ type: string; tool_use_id?: string; content?: unknown; is_error?: boolean }> };
      }).message;
      if (!Array.isArray(um.content)) return;
      for (const block of um.content) {
        if (block.type !== 'tool_result') continue;
        const tuId = block.tool_use_id ?? '';
        if (this.claimedToolIds.has(tuId)) continue;
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
      const r = msg as {
        duration_ms?: number;
        total_cost_usd?: number;
        num_turns?: number;
      };
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
