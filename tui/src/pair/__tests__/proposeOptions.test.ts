// Tests the propose_options handler in isolation, plus its integration
// through core Session via customToolHandlers. These were the "burned-the-
// fingers" cases that motivated the runtime suppression of malformed
// propose_options validation errors.

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
        options: [
          { title: 'A', body: 'first' },
          { title: 'B', body: 'second' },
        ],
        private_notes: { best_index: 0, trap_flaw: 'b is wrong' },
      },
    });

    expect(result).toEqual({
      kind: 'options',
      toolUseId: 'toolu_1',
      options: [
        { title: 'A', body: 'first' },
        { title: 'B', body: 'second' },
      ],
      privateNotes: { bestIndex: 0, trapFlaw: 'b is wrong' },
    });
  });

  it('returns null for malformed args (suppresses but emits nothing)', () => {
    const result = proposeOptionsHandler({
      id: 'toolu_2',
      name: FULL_PROPOSE_TOOL_NAME,
      input: { options: 'not an array' },
    });
    expect(result).toBeNull();
  });

  it('returns null when array length is wrong', () => {
    const result = proposeOptionsHandler({
      id: 'toolu_3',
      name: FULL_PROPOSE_TOOL_NAME,
      input: { options: [{ title: 'lonely', body: 'option' }] },
    });
    expect(result).toBeNull();
  });

  it('returns null when option entries are missing title/body', () => {
    const result = proposeOptionsHandler({
      id: 'toolu_4',
      name: FULL_PROPOSE_TOOL_NAME,
      input: {
        options: [
          { title: 'A' },
          { title: 'B', body: 'fine' },
        ],
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
              options: [
                { title: 'A', body: 'first' },
                { title: 'B', body: 'second' },
              ],
              private_notes: { best_index: 0, trap_flaw: '' },
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
      privateNotes: { bestIndex: 0, trapFlaw: '' },
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
            input: { options: 'not an array' },
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
        delta: { type: 'input_json_delta', partial_json: '{"options":[' },
      },
    });
    session.translate({
      type: 'stream_event',
      event: { type: 'content_block_stop', index: 0 },
    });

    expect(events).toHaveLength(0);
  });
});
