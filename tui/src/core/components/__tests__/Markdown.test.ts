// Pure-logic tests for the Markdown parser. Critical: the streaming use-case
// receives partial input mid-tick (e.g. an unclosed `\``) and the parser
// must always advance — an earlier infinite-loop bug here locked up the
// entire UI.

import { describe, expect, it } from 'bun:test';
import { isDiffBlock, splitBlocks, splitInline } from '../Markdown';

describe('splitInline', () => {
  it('returns plain text for input with no special chars', () => {
    expect(splitInline('hello world')).toEqual([
      { kind: 'text', value: 'hello world' },
    ]);
  });

  it('extracts single inline code', () => {
    expect(splitInline('see `foo` now')).toEqual([
      { kind: 'text', value: 'see ' },
      { kind: 'code', value: 'foo' },
      { kind: 'text', value: ' now' },
    ]);
  });

  it('extracts bold and italic', () => {
    expect(splitInline('a **b** c *d* e')).toEqual([
      { kind: 'text', value: 'a ' },
      { kind: 'bold', value: 'b' },
      { kind: 'text', value: ' c ' },
      { kind: 'em', value: 'd' },
      { kind: 'text', value: ' e' },
    ]);
  });

  it('does not infinite-loop on unclosed backtick (streaming partial input)', () => {
    // The bug we hit: indexOf returned -1, j stayed at i, loop spun forever.
    // We expect the parser to emit the rest as plain text and terminate.
    const out = splitInline('foo `bar');
    expect(out.length).toBeGreaterThan(0);
    expect(out.map((s) => s.value).join('')).toBe('foo `bar');
  });

  it('does not infinite-loop on unclosed bold', () => {
    const out = splitInline('hi **partial');
    expect(out.length).toBeGreaterThan(0);
    expect(out.map((s) => s.value).join('')).toBe('hi **partial');
  });

  it('does not infinite-loop on unclosed em', () => {
    const out = splitInline('hi *partial');
    expect(out.length).toBeGreaterThan(0);
    expect(out.map((s) => s.value).join('')).toBe('hi *partial');
  });

  it('handles empty input', () => {
    expect(splitInline('')).toEqual([]);
  });

  it('handles input that is only special chars', () => {
    // Should not hang.
    const out = splitInline('***');
    expect(out.length).toBeGreaterThan(0);
  });

  it('handles back-to-back inline elements', () => {
    expect(splitInline('`a``b`')).toEqual([
      { kind: 'code', value: 'a' },
      { kind: 'code', value: 'b' },
    ]);
  });
});

describe('splitBlocks', () => {
  it('returns one prose block for plain text', () => {
    const out = splitBlocks('Hello world');
    expect(out).toEqual([{ kind: 'prose', text: 'Hello world' }]);
  });

  it('separates a fenced block from surrounding prose', () => {
    const out = splitBlocks('Before\n```py\nx = 1\n```\nAfter');
    expect(out).toEqual([
      { kind: 'prose', text: 'Before' },
      { kind: 'fence', lang: 'py', body: 'x = 1' },
      { kind: 'prose', text: 'After' },
    ]);
  });

  it('handles a fence at the start', () => {
    const out = splitBlocks('```diff\n+a\n```');
    expect(out).toEqual([{ kind: 'fence', lang: 'diff', body: '+a' }]);
  });

  it('treats an unclosed fence as a fence body to EOF (mid-stream)', () => {
    // Streaming: closing fence hasn't arrived yet. Should not crash.
    const out = splitBlocks('```diff\n+a\n+b');
    expect(out).toHaveLength(1);
    expect(out[0]?.kind).toBe('fence');
    if (out[0]?.kind === 'fence') {
      expect(out[0].body).toBe('+a\n+b');
    }
  });

  it('handles tilde fences too', () => {
    const out = splitBlocks('~~~py\nx\n~~~');
    expect(out).toEqual([{ kind: 'fence', lang: 'py', body: 'x' }]);
  });
});

describe('isDiffBlock', () => {
  it('recognizes explicit `diff` lang', () => {
    expect(isDiffBlock('diff', '')).toBe(true);
  });

  it('recognizes hunk header even without lang', () => {
    expect(isDiffBlock('', '@@ -1,1 +1,2 @@\n+foo')).toBe(true);
  });

  it('recognizes file-meta header even without lang', () => {
    expect(isDiffBlock('', '+++ foo.py\n+x')).toBe(true);
  });

  it('rejects regular language with no diff markers', () => {
    expect(isDiffBlock('python', 'def foo():\n  pass')).toBe(false);
  });

  it('rejects empty body', () => {
    expect(isDiffBlock('', '')).toBe(false);
  });
});
