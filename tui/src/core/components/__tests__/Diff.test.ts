import { describe, expect, it } from 'bun:test';
import { countAddRemove, detectLang, lineDiff, parse } from '../Diff';

describe('detectLang', () => {
  it('detects python from `+++ filename.py`', () => {
    expect(detectLang('+++ tic_tac_toe.py\n@@ -1,1 +1,2 @@\n+foo')).toBe('python');
  });

  it('detects javascript from .js', () => {
    expect(detectLang('+++ a/b/foo.js\n@@ -1,1 +1,2 @@\n+x')).toBe('javascript');
  });

  it('detects typescript from .tsx', () => {
    expect(detectLang('+++ App.tsx\n+x')).toBe('typescript');
  });

  it('strips a/ b/ prefixes from filenames', () => {
    expect(detectLang('+++ b/path/to/foo.go\n+x')).toBe('go');
  });

  it('returns undefined when no header', () => {
    expect(detectLang('@@ -1,1 +1,1 @@\n+x')).toBeUndefined();
  });

  it('returns undefined for unknown extension', () => {
    expect(detectLang('+++ foo.xyz\n+x')).toBeUndefined();
  });
});

describe('parse', () => {
  it('parses a simple all-add diff', () => {
    const out = parse('+++ foo.py\n@@ -0,0 +1,2 @@\n+def f():\n+    pass');
    expect(out).toHaveLength(4);
    expect(out[0]).toEqual({ kind: 'meta', num: null, text: '+++ foo.py' });
    expect(out[1]).toEqual({ kind: 'hunk', num: null, text: '@@ -0,0 +1,2 @@' });
    expect(out[2]).toEqual({ kind: 'add', num: 1, text: 'def f():' });
    expect(out[3]).toEqual({ kind: 'add', num: 2, text: '    pass' });
  });

  it('tracks separate old/new line counters for - and + lines', () => {
    const out = parse('@@ -3,2 +3,2 @@\n-old1\n-old2\n+new1\n+new2');
    const dels = out.filter((l) => l.kind === 'del');
    const adds = out.filter((l) => l.kind === 'add');
    expect(dels.map((l) => l.num)).toEqual([3, 4]);
    expect(adds.map((l) => l.num)).toEqual([3, 4]);
  });

  it('numbers context lines from the new-side counter', () => {
    const out = parse('@@ -1,3 +1,3 @@\n ctx1\n-old\n+new\n ctx2');
    const ctx = out.filter((l) => l.kind === 'ctx');
    expect(ctx.map((l) => l.num)).toEqual([1, 3]);
    // Both ctx lines after the @@: first is line 1; old line 2 is removed,
    // new line 2 is added, then ctx is line 3.
  });

  it('handles diffs with no hunk header (line numbers null)', () => {
    const out = parse('+a\n+b\n+c');
    expect(out.map((l) => l.num)).toEqual([null, null, null]);
  });
});


describe('lineDiff', () => {
  it('returns all eq when both sides are identical', () => {
    const ops = lineDiff(['a', 'b', 'c'], ['a', 'b', 'c']);
    expect(ops.every((op) => op.kind === 'eq')).toBe(true);
    expect(countAddRemove(ops)).toEqual({ added: 0, removed: 0 });
  });

  it('treats unchanged leading lines as eq when only appending (the bug)', () => {
    // Regression: old="a\nb", new="a\nb\nc" used to render every old line as
    // `-` and every new line as `+`, showing the leading 2 lines twice.
    const ops = lineDiff(['a', 'b'], ['a', 'b', 'c']);
    expect(ops).toEqual([
      { kind: 'eq', line: 'a' },
      { kind: 'eq', line: 'b' },
      { kind: 'add', line: 'c' },
    ]);
    expect(countAddRemove(ops)).toEqual({ added: 1, removed: 0 });
  });

  it('handles pure deletion', () => {
    const ops = lineDiff(['a', 'b', 'c'], ['a', 'c']);
    expect(countAddRemove(ops)).toEqual({ added: 0, removed: 1 });
    // 'a' and 'c' should be eq.
    expect(ops.filter((o) => o.kind === 'eq').map((o) => o.line)).toEqual(['a', 'c']);
    expect(ops.filter((o) => o.kind === 'del').map((o) => o.line)).toEqual(['b']);
  });

  it('handles a mid-line replacement', () => {
    const ops = lineDiff(['a', 'b', 'c'], ['a', 'x', 'c']);
    expect(countAddRemove(ops)).toEqual({ added: 1, removed: 1 });
    expect(ops.filter((o) => o.kind === 'eq').map((o) => o.line)).toEqual(['a', 'c']);
    expect(ops.filter((o) => o.kind === 'add').map((o) => o.line)).toEqual(['x']);
    expect(ops.filter((o) => o.kind === 'del').map((o) => o.line)).toEqual(['b']);
  });

  it('handles empty old (Write-style)', () => {
    const ops = lineDiff([], ['a', 'b']);
    expect(ops).toEqual([
      { kind: 'add', line: 'a' },
      { kind: 'add', line: 'b' },
    ]);
  });

  it('handles empty new', () => {
    const ops = lineDiff(['a', 'b'], []);
    expect(ops).toEqual([
      { kind: 'del', line: 'a' },
      { kind: 'del', line: 'b' },
    ]);
  });
});
