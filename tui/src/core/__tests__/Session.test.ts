// Tests core Session.translate() with synthetic SDK messages. These cover
// only the generic CC-clone behaviour — propose_options-specific logic
// lives in pair/ and is tested in pair/__tests__/proposeOptions.test.ts.

import { describe, expect, it } from 'bun:test';
import { Session } from '../Session';
import { type CoreAgentEvent } from '../types';

function captureEvents(opts?: { customToolHandlers?: Record<string, () => unknown> }): {
  session: Session;
  events: CoreAgentEvent[];
} {
  const events: CoreAgentEvent[] = [];
  const session = new Session({
    systemPrompt: 'test',
    customToolHandlers: opts?.customToolHandlers as never,
  });
  session.onEvent((ev) => events.push(ev as CoreAgentEvent));
  return { session, events };
}


describe('Session.translate — ToolSearch (SDK-internal)', () => {
  it('hides ToolSearch tool_use_start', () => {
    const { session, events } = captureEvents();

    session.translate({
      type: 'stream_event',
      event: {
        type: 'content_block_start',
        index: 0,
        content_block: { type: 'tool_use', id: 'toolu_search_1', name: 'ToolSearch' },
      },
    });

    expect(events).toHaveLength(0);
  });

  it('hides ToolSearch tool_result', () => {
    const { session, events } = captureEvents();

    session.translate({
      type: 'assistant',
      message: {
        content: [
          { type: 'tool_use', id: 'toolu_search_2', name: 'ToolSearch', input: {} },
        ],
      },
    });
    session.translate({
      type: 'user',
      message: {
        content: [
          { type: 'tool_result', tool_use_id: 'toolu_search_2', content: 'ok', is_error: false },
        ],
      },
    });

    expect(events).toHaveLength(0);
  });
});


describe('Session.translate — regular tools', () => {
  it('emits tool_use_start from the stream_event', () => {
    const { session, events } = captureEvents();

    session.translate({
      type: 'stream_event',
      event: {
        type: 'content_block_start',
        index: 0,
        content_block: { type: 'tool_use', id: 'toolu_b1', name: 'Bash' },
      },
    });

    expect(events).toEqual([
      { kind: 'tool_use_start', id: 'toolu_b1', name: 'Bash', input: {} },
    ]);
  });

  it('emits tool_use_done from the assistant message with the full input', () => {
    const { session, events } = captureEvents();

    session.translate({
      type: 'assistant',
      message: {
        content: [
          { type: 'tool_use', id: 'toolu_b1', name: 'Bash', input: { command: 'ls' } },
        ],
      },
    });

    expect(events).toEqual([
      { kind: 'tool_use_done', id: 'toolu_b1', input: { command: 'ls' } },
    ]);
  });

  it('emits tool_result with name resolved from the prior tool_use', () => {
    const { session, events } = captureEvents();

    session.translate({
      type: 'assistant',
      message: {
        content: [
          { type: 'tool_use', id: 'toolu_b2', name: 'Bash', input: { command: 'ls' } },
        ],
      },
    });
    events.length = 0;

    session.translate({
      type: 'user',
      message: {
        content: [
          { type: 'tool_result', tool_use_id: 'toolu_b2', content: 'foo\nbar\n', is_error: false },
        ],
      },
    });

    expect(events).toHaveLength(1);
    expect(events[0]).toMatchObject({
      kind: 'tool_result',
      toolUseId: 'toolu_b2',
      name: 'Bash',
      text: 'foo\nbar\n',
      isError: false,
    });
  });

  it('extracts text from array-shaped tool_result content', () => {
    const { session, events } = captureEvents();
    session.translate({
      type: 'user',
      message: {
        content: [
          {
            type: 'tool_result',
            tool_use_id: 'toolu_x',
            content: [{ text: 'hello' }, { text: ' world' }],
            is_error: false,
          },
        ],
      },
    });
    expect(events).toHaveLength(1);
    expect((events[0] as { text: string }).text).toBe('hello world');
  });
});


describe('Session.translate — text streaming', () => {
  it('emits text_delta on content_block_delta of type text_delta', () => {
    const { session, events } = captureEvents();

    session.translate({
      type: 'stream_event',
      event: {
        type: 'content_block_delta',
        index: 0,
        delta: { type: 'text_delta', text: 'hello' },
      },
    });

    expect(events).toEqual([{ kind: 'text_delta', text: 'hello' }]);
  });

  it('emits text_block_done on content_block_stop', () => {
    const { session, events } = captureEvents();

    session.translate({
      type: 'stream_event',
      event: { type: 'content_block_stop', index: 0 },
    });

    expect(events).toEqual([{ kind: 'text_block_done' }]);
  });
});


describe('Session.translate — result', () => {
  it('emits a result event with timing and cost', () => {
    const { session, events } = captureEvents();

    session.translate({
      type: 'result',
      duration_ms: 1234,
      total_cost_usd: 0.0042,
      num_turns: 1,
    });

    expect(events).toEqual([
      {
        kind: 'result',
        durationMs: 1234,
        totalCostUsd: 0.0042,
        numTurns: 1,
      },
    ]);
  });
});


describe('Session.translate — customToolHandlers extension', () => {
  it('routes a registered tool name to its handler and emits the returned event', () => {
    const events: unknown[] = [];
    const session = new Session({
      systemPrompt: 'test',
      customToolHandlers: {
        my_custom_tool: (block) => ({
          kind: 'custom_event',
          input: block.input,
        }),
      },
    });
    session.onEvent((ev) => events.push(ev));

    session.translate({
      type: 'assistant',
      message: {
        content: [
          { type: 'tool_use', id: 'toolu_x', name: 'my_custom_tool', input: { foo: 1 } },
        ],
      },
    });

    expect(events).toEqual([{ kind: 'custom_event', input: { foo: 1 } }]);
  });

  it('claims the tool_use_id even when the handler returns null (suppresses tool_result)', () => {
    const events: unknown[] = [];
    const session = new Session({
      systemPrompt: 'test',
      customToolHandlers: {
        my_custom_tool: () => null,
      },
    });
    session.onEvent((ev) => events.push(ev));

    session.translate({
      type: 'assistant',
      message: {
        content: [
          { type: 'tool_use', id: 'toolu_y', name: 'my_custom_tool', input: {} },
        ],
      },
    });
    session.translate({
      type: 'user',
      message: {
        content: [
          {
            type: 'tool_result',
            tool_use_id: 'toolu_y',
            content: 'should be suppressed',
            is_error: true,
          },
        ],
      },
    });

    expect(events).toHaveLength(0);
  });

  it('suppresses stream events for custom tools (no tool_use_start surfaces)', () => {
    const events: unknown[] = [];
    const session = new Session({
      systemPrompt: 'test',
      customToolHandlers: { my_custom_tool: () => null },
    });
    session.onEvent((ev) => events.push(ev));

    session.translate({
      type: 'stream_event',
      event: {
        type: 'content_block_start',
        index: 5,
        content_block: { type: 'tool_use', id: 'toolu_z', name: 'my_custom_tool' },
      },
    });
    session.translate({
      type: 'stream_event',
      event: {
        type: 'content_block_delta',
        index: 5,
        delta: { type: 'input_json_delta', partial_json: '{' },
      },
    });
    session.translate({
      type: 'stream_event',
      event: { type: 'content_block_stop', index: 5 },
    });

    expect(events).toHaveLength(0);
  });
});
