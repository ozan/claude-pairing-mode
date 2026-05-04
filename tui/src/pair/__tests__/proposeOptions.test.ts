// Tests the propose_options handler in isolation, plus its integration
// through core Session via customToolHandlers.

import { describe, expect, it } from 'bun:test';
import { Session } from '../../core/Session';
import {
  FULL_PROPOSE_TOOL_NAME,
  proposeOptionsHandler,
  type OptionsEvent,
} from '../proposeOptions';

function pairSession() {
  const events: (OptionsEvent | unknown)[] = [];
  const session = new Session<OptionsEvent>({
    systemPrompt: 'test',
    customToolHandlers: { [FULL_PROPOSE_TOOL_NAME]: proposeOptionsHandler },
  });
  session.onEvent((ev) => events.push(ev));
  return { session, events };
}


describe('proposeOptionsHandler', () => {
  it('returns an options event for a well-formed call', () => {
    const result = proposeOptionsHandler({
      id: 'toolu_1',
      name: FULL_PROPOSE_TOOL_NAME,
      input: {
        option_a_title: 'A',
        option_a_body: 'first',
        option_b_title: 'B',
        option_b_body: 'second',
        best_letter: 'A',
        rationale: 'A is best because foo',
      },
    });

    expect(result).toEqual({
      kind: 'options',
      toolUseId: 'toolu_1',
      options: [
        { title: 'A', body: 'first' },
        { title: 'B', body: 'second' },
      ],
      privateNotes: { bestIndex: 0, rationale: 'A is best because foo' },
    });
  });

  it('returns null when a required string field is missing', () => {
    const result = proposeOptionsHandler({
      id: 'toolu_2',
      name: FULL_PROPOSE_TOOL_NAME,
      input: {
        option_a_title: 'A',
        option_a_body: 'first',
        option_b_title: 'B',
        // option_b_body missing
      },
    });
    expect(result).toBeNull();
  });

  it('omits private notes when best_index/rationale are absent', () => {
    const result = proposeOptionsHandler({
      id: 'toolu_3',
      name: FULL_PROPOSE_TOOL_NAME,
      input: {
        option_a_title: 'A',
        option_a_body: 'first',
        option_b_title: 'B',
        option_b_body: 'second',
      },
    });
    expect(result).not.toBeNull();
    expect(result?.options).toHaveLength(2);
    expect(result?.privateNotes).toEqual({ bestIndex: undefined, rationale: undefined });
  });

  it('returns null when a field is the wrong type', () => {
    const result = proposeOptionsHandler({
      id: 'toolu_4',
      name: FULL_PROPOSE_TOOL_NAME,
      input: {
        option_a_title: 'A',
        option_a_body: 42, // not a string
        option_b_title: 'B',
        option_b_body: 'second',
      },
    });
    expect(result).toBeNull();
  });
});


describe('Session integration with proposeOptionsHandler', () => {
  it('emits a synthesized options event for a well-formed propose_options assistant tool_use', () => {
    const { session, events } = pairSession();

    session.translate({
      type: 'assistant',
      message: {
        content: [
          {
            type: 'tool_use',
            id: 'toolu_a',
            name: FULL_PROPOSE_TOOL_NAME,
            input: {
              option_a_title: 'A',
              option_a_body: 'first',
              option_b_title: 'B',
              option_b_body: 'second',
              best_letter: 'A',
              rationale: '',
            },
          },
        ],
      },
    });

    expect(events).toHaveLength(1);
    expect(events[0]).toEqual({
      kind: 'options',
      toolUseId: 'toolu_a',
      options: [
        { title: 'A', body: 'first' },
        { title: 'B', body: 'second' },
      ],
      privateNotes: { bestIndex: 0, rationale: '' },
    });
  });

  it('does not emit for malformed propose_options (no Tool({}) MCP-error pill leaks)', () => {
    const { session, events } = pairSession();

    session.translate({
      type: 'assistant',
      message: {
        content: [
          {
            type: 'tool_use',
            id: 'toolu_b',
            name: FULL_PROPOSE_TOOL_NAME,
            input: { option_a_title: 'A' }, // missing required fields
          },
        ],
      },
    });
    // SDK then surfaces the validation error as a tool_result.
    session.translate({
      type: 'user',
      message: {
        content: [
          {
            type: 'tool_result',
            tool_use_id: 'toolu_b',
            content: 'MCP error -32602: Input validation error',
            is_error: true,
          },
        ],
      },
    });

    expect(events).toHaveLength(0);
  });

  it('suppresses propose_options stream events (no flicker before assistant message)', () => {
    const { session, events } = pairSession();

    session.translate({
      type: 'stream_event',
      event: {
        type: 'content_block_start',
        index: 0,
        content_block: { type: 'tool_use', id: 'toolu_c', name: FULL_PROPOSE_TOOL_NAME },
      },
    });
    session.translate({
      type: 'stream_event',
      event: {
        type: 'content_block_delta',
        index: 0,
        delta: { type: 'input_json_delta', partial_json: '{"option_a_title":"A"' },
      },
    });
    session.translate({
      type: 'stream_event',
      event: { type: 'content_block_stop', index: 0 },
    });

    expect(events).toHaveLength(0);
  });
});
