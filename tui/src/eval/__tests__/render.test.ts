// Verifies the user-vs-human render distinction. Crucial: when
// `forUser: true`, Sonnet's thinking blocks must NOT appear in the
// rendered output. Without this, the user-model (Haiku) saw Sonnet's
// preferred-option reasoning and metagamed its choices, corrupting
// every prior eval result.

import { describe, expect, it } from 'bun:test';
import { renderTurn, type AnyEvent } from '../render';

const sampleEvents: AnyEvent[] = [
  { kind: 'thinking_block_done', text: 'I prefer option B because it is the optimal solution.' },
  { kind: 'text_delta', text: 'Here are two approaches: ' },
  { kind: 'text_block_done' },
  { kind: 'options', toolUseId: 't1', options: [
    { title: 'Brute force', body: 'O(n²) loop' },
    { title: 'Two pointers', body: 'O(n) optimal' },
  ], privateNotes: { bestIndex: 1, rationale: 'B is faster' } },
  { kind: 'result', durationMs: 100, totalCostUsd: 0, numTurns: 1 },
];

describe('renderTurn forUser flag', () => {
  it('default render (forUser=false) INCLUDES thinking blocks', () => {
    const out = renderTurn(sampleEvents);
    expect(out).toContain('Thinking:');
    expect(out).toContain('option B');
  });

  it('forUser=true STRIPS thinking blocks (no metagaming leak)', () => {
    const out = renderTurn(sampleEvents, { forUser: true });
    expect(out).not.toContain('Thinking:');
    expect(out).not.toContain('option B because it is the optimal');
  });

  it('forUser=true STILL renders public content (text + options)', () => {
    const out = renderTurn(sampleEvents, { forUser: true });
    expect(out).toContain('Here are two approaches');
    expect(out).toContain('Brute force');
    expect(out).toContain('Two pointers');
    expect(out).toContain('[A]');
    expect(out).toContain('[B]');
  });

  it('forUser=true does NOT leak privateNotes (rationale, bestIndex)', () => {
    const out = renderTurn(sampleEvents, { forUser: true });
    expect(out).not.toContain('B is faster');
    expect(out).not.toContain('bestIndex');
    expect(out).not.toContain('rationale');
  });

  it('handles thinking-only turns (no text/options) cleanly', () => {
    const events: AnyEvent[] = [
      { kind: 'thinking_block_done', text: 'private reasoning' },
      { kind: 'result', durationMs: 1, totalCostUsd: 0, numTurns: 1 },
    ];
    expect(renderTurn(events)).toContain('Thinking:');
    expect(renderTurn(events, { forUser: true })).not.toContain('Thinking:');
    expect(renderTurn(events, { forUser: true })).not.toContain('private reasoning');
  });
});
