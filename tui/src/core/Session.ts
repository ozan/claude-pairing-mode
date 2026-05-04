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
  type CanUseTool,
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


// Some tool errors come back wrapped in `<tool_use_error>...</tool_use_error>`
// (e.g. Write's "File has not been read yet"), others come as plain prose
// (e.g. Read's "File does not exist."). Strip the wrapper so the rendered
// error line is consistent.
function stripToolUseErrorWrapper(text: string): string {
  const m = text.match(/^<tool_use_error>([\s\S]*)<\/tool_use_error>\s*$/);
  return m ? m[1]!.trim() : text;
}


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
  disallowedTools?: string[];
  /** Working directory the SDK uses for tool calls (defaults to process.cwd()). */
  cwd?: string;
  /** Override the model id (defaults to whatever the SDK chooses). */
  model?: string;
  /**
   * Output style name (e.g. 'Learning', 'Explanatory', 'default'). Only
   * effective when paired with `settingSources` containing 'project' or
   * 'user' AND a `.claude/settings.json` with `outputStyle: <name>` exists
   * at the corresponding path. Per-query alone is silently ignored by the
   * SDK — see diag-init.ts for the experiment that confirmed this.
   */
  outputStyle?: string;
  /**
   * Where the SDK loads filesystem settings from. Defaults to none, meaning
   * settings.json files are ignored. Pass ['project'] to read
   * `<cwd>/.claude/settings.json` — required to actually activate
   * outputStyle.
   */
  settingSources?: ('user' | 'project' | 'local')[];
  /** Hard cap on spend for this session (USD). SDK stops the query if exceeded. */
  maxBudgetUsd?: number;
  /** Hard cap on the number of agentic turns. Prevents runaway tool loops. */
  maxTurns?: number;
  /**
   * Map of tool name (full SDK name like `mcp__server__tool_name`) → handler.
   * When the assistant calls a tool whose name is a key here, the handler
   * gets the tool_use block and decides what (if anything) to emit. Stream
   * events for these tools' content blocks are also suppressed (no
   * tool_use_start), and their tool_results are swallowed.
   */
  customToolHandlers?: Record<string, CustomToolHandler<E>>;
  /**
   * Optional callback the SDK invokes before dispatching each tool call.
   * Returning `{ behavior: 'allow', updatedInput }` rewrites args before
   * dispatch — the lever we use to repair the model's JSON-string args
   * (Sonnet sometimes serializes `options` as a JSON string instead of an
   * array, which the SDK then rejects with "No such tool available"
   * before reaching the MCP tool body). Note: requires `permissionMode`
   * other than `bypassPermissions` for the callback to fire.
   */
  canUseTool?: CanUseTool;
};


export type InitInfo = {
  tools: string[];
  mcpServers: { name: string; status: string }[];
};

export class Session<E = never> {
  private queue = new UserMessageQueue();
  private listener: ((ev: CoreAgentEvent | E) => void) | null = null;
  private rawListener: ((msg: unknown) => void) | null = null;
  private consumePromise: Promise<void> | null = null;
  private isAborted = false;
  private abortController: AbortController | null = null;
  // Resolved on the first `system/init` message so callers can verify MCP
  // server registration succeeded before sending any prompts. The agent
  // SDK occasionally fails to register in-process MCP servers; the eval
  // uses this to detect-and-retry rather than running with a broken tool
  // list.
  private initResolve: ((info: InitInfo) => void) | null = null;
  readonly initialized: Promise<InitInfo>;

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
  // Stream indices belonging to thinking blocks; accumulator keyed by index.
  private thinkingIndices = new Set<number>();
  private thinkingAccum = new Map<number, string>();

  private turnStartedAt = Date.now();

  constructor(private opts: SessionOptions<E>) {
    this.initialized = new Promise<InitInfo>((resolve) => {
      this.initResolve = resolve;
    });
  }

  /** Begin consuming the long-running Query. Call once at app start. */
  start(): void {
    if (this.consumePromise) return;
    this.isAborted = false;
    this.abortController = new AbortController();
    // canUseTool only fires when permissionMode != 'bypassPermissions'.
    // Default to 'default' if a canUseTool was provided, else
    // 'bypassPermissions' for the original frictionless behavior.
    const permissionMode = this.opts.canUseTool ? 'default' : 'bypassPermissions';
    const q = query({
      prompt: this.queue,
      options: {
        mcpServers: this.opts.mcpServers ?? {},
        systemPrompt: this.opts.systemPrompt,
        permissionMode,
        allowedTools: this.opts.allowedTools ?? ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash'],
        disallowedTools: this.opts.disallowedTools ?? [],
        includePartialMessages: true,
        abortController: this.abortController,
        ...(this.opts.canUseTool ? { canUseTool: this.opts.canUseTool } : {}),
        ...(this.opts.cwd ? { cwd: this.opts.cwd } : {}),
        ...(this.opts.model ? { model: this.opts.model } : {}),
        ...(this.opts.outputStyle ? { outputStyle: this.opts.outputStyle } : {}),
        ...(this.opts.settingSources ? { settingSources: this.opts.settingSources } : {}),
        ...(this.opts.maxBudgetUsd !== undefined ? { maxBudgetUsd: this.opts.maxBudgetUsd } : {}),
        ...(this.opts.maxTurns !== undefined ? { maxTurns: this.opts.maxTurns } : {}),
      },
    });

    this.consumePromise = (async () => {
      try {
        for await (const msg of q) {
          if (this.isAborted) break;
          this.rawListener?.(msg);
          // Capture the init message for caller-side MCP-status checking.
          const m = msg as { type?: string; subtype?: string; tools?: string[]; mcp_servers?: Array<{ name: string; status: string }> };
          if (m.type === 'system' && m.subtype === 'init' && this.initResolve) {
            this.initResolve({
              tools: m.tools ?? [],
              mcpServers: m.mcp_servers ?? [],
            });
            this.initResolve = null;
          }
          this.translate(msg);
        }
      } catch (e) {
        // AbortError is expected when the user interrupts — not a real error.
        const err = e as Error;
        if (err.name !== 'AbortError') {
          this.emit({ kind: 'error', message: `${err.name}: ${err.message}` } as CoreAgentEvent);
        }
      }
    })();
  }

  /** Subscribe to events. Only one listener supported. */
  onEvent(handler: (ev: CoreAgentEvent | E) => void): void {
    this.listener = handler;
  }

  /**
   * Subscribe to raw SDK messages (pre-translation). Used by the eval to
   * write a verbose jsonl alongside the translated event stream — necessary
   * because Session suppresses tool_use_start / tool_results for
   * custom-handled tools, so malformed `propose_options` calls would be
   * invisible in the translated stream alone. Only one listener supported.
   */
  onRawMessage(handler: (msg: unknown) => void): void {
    this.rawListener = handler;
  }

  /** Send a user prompt; events flow back via the listener. */
  send(text: string): void {
    this.turnStartedAt = Date.now();
    this.isAborted = false;
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

  /** Cancel the current turn: abort the HTTP request and emit a cancellation result. */
  abort(): void {
    this.isAborted = true;
    this.abortController?.abort();
    this.emit({ kind: 'result', durationMs: Date.now() - this.turnStartedAt, totalCostUsd: 0, numTurns: 0 } as CoreAgentEvent);
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
          delta?: { type: string; text?: string; thinking?: string };
        };
      }).event;
      const et = ev.type;

      if (et === 'message_start') {
        this.suppressedIndices.clear();
        this.thinkingIndices.clear();
        this.thinkingAccum.clear();
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
        if (cb.type === 'thinking') {
          if (idx !== undefined) {
            this.thinkingIndices.add(idx);
            this.thinkingAccum.set(idx, '');
          }
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
        if (d.type === 'thinking_delta' && ev.index !== undefined && this.thinkingIndices.has(ev.index)) {
          const prev = this.thinkingAccum.get(ev.index) ?? '';
          this.thinkingAccum.set(ev.index, prev + (d.thinking ?? ''));
          return;
        }
      }
      if (et === 'content_block_stop') {
        if (ev.index !== undefined && this.suppressedIndices.has(ev.index)) return;
        if (ev.index !== undefined && this.thinkingIndices.has(ev.index)) {
          const text = this.thinkingAccum.get(ev.index) ?? '';
          this.thinkingIndices.delete(ev.index);
          this.thinkingAccum.delete(ev.index);
          this.emit({ kind: 'thinking_block_done', text });
          return;
        }
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
          text: stripToolUseErrorWrapper(text),
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
