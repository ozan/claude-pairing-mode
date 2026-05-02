// Render tests for OptionsBlock (the 2-column rounded-border panel). These
// guard against layout regressions: closed borders on every panel,
// equalized panel heights even when bodies differ in length, content
// wrapping inside the column, and graceful handling of edge cases (empty
// body, no-break long words, multi-paragraph, diff-only bodies).

import React from 'react';
import { describe, expect, it } from 'bun:test';
import { render } from 'ink-testing-library';
import { OptionsBlock } from '../OptionsBlock';

function strip(s: string | undefined): string {
  return (s ?? '').replace(/\x1B\[[0-9;]*[A-Za-z]/g, '');
}

function lines(out: string): string[] {
  return out.split('\n');
}

// All the round-border characters we expect to see.
const TOP_LEFT = '╭';
const TOP_RIGHT = '╮';
const BOTTOM_LEFT = '╰';
const BOTTOM_RIGHT = '╯';
const HORIZ = '─';
const VERT = '│';


describe('OptionsBlock — borders', () => {
  it('draws a complete rounded border around each panel', () => {
    const out = strip(
      render(
        <OptionsBlock
          options={[
            { title: 'A', body: 'short' },
            { title: 'B', body: 'short' },
          ]}
        />,
      ).lastFrame(),
    );
    const ls = lines(out);
    // Should have two top corners on the same row, two bottom corners on
    // the same row.
    const top = ls.find((l) => l.includes(TOP_LEFT));
    const bottom = ls.find((l) => l.includes(BOTTOM_LEFT));
    expect(top).toBeDefined();
    expect(bottom).toBeDefined();
    expect((top ?? '').match(/╭/g)?.length).toBe(2);
    expect((top ?? '').match(/╮/g)?.length).toBe(2);
    expect((bottom ?? '').match(/╰/g)?.length).toBe(2);
    expect((bottom ?? '').match(/╯/g)?.length).toBe(2);
  });

  it('places vertical bars on every body row of both panels', () => {
    const out = strip(
      render(
        <OptionsBlock
          options={[
            { title: 'A', body: 'one\ntwo\nthree' },
            { title: 'B', body: 'short' },
          ]}
        />,
      ).lastFrame(),
    );
    const ls = lines(out);
    // Every non-border row should have at least 2 vertical bars (one per
    // panel side, total 4 bars per row inside the box: open|content|close|gap|open|content|close).
    // We just check >= 2 to be conservative.
    const bodyRows = ls.filter(
      (l) => l.length > 0 && !l.includes(TOP_LEFT) && !l.includes(BOTTOM_LEFT),
    );
    for (const r of bodyRows) {
      const bars = r.match(/│/g)?.length ?? 0;
      expect(bars).toBeGreaterThanOrEqual(2);
    }
  });
});


describe('OptionsBlock — equal heights', () => {
  it('makes both panels the same height when one body is much longer', () => {
    const out = strip(
      render(
        <OptionsBlock
          options={[
            { title: 'A', body: 'one' },
            {
              title: 'B',
              body: 'a long body that should wrap to several lines and stretch the panel height substantially beyond the short side',
            },
          ]}
        />,
      ).lastFrame(),
    );
    const ls = lines(out);
    // Find the row that has the top corners and the row that has the
    // bottom corners. They should each appear exactly once → both panels
    // start and end at the same row.
    const topRows = ls.filter((l) => l.includes(TOP_LEFT)).length;
    const bottomRows = ls.filter((l) => l.includes(BOTTOM_LEFT)).length;
    expect(topRows).toBe(1);
    expect(bottomRows).toBe(1);
  });
});


describe('OptionsBlock — content', () => {
  it('shows both titles with letter prefixes', () => {
    const out = strip(
      render(
        <OptionsBlock
          options={[
            { title: 'Recursive', body: 'x' },
            { title: 'Iterative', body: 'x' },
          ]}
        />,
      ).lastFrame(),
    );
    expect(out).toContain('A.  Recursive');
    expect(out).toContain('B.  Iterative');
  });

  it('renders option bodies', () => {
    const out = strip(
      render(
        <OptionsBlock
          options={[
            { title: 'A', body: 'alpha body text' },
            { title: 'B', body: 'beta body text' },
          ]}
        />,
      ).lastFrame(),
    );
    expect(out).toContain('alpha body text');
    expect(out).toContain('beta body text');
  });

  it('renders diff blocks inside an option body', () => {
    const out = strip(
      render(
        <OptionsBlock
          options={[
            {
              title: 'A',
              body: '```diff\n+++ foo.py\n@@ -0,0 +1,1 @@\n+def f(): pass\n```',
            },
            { title: 'B', body: 'no diff' },
          ]}
        />,
      ).lastFrame(),
    );
    expect(out).toContain('@@ -0,0 +1,1 @@');
    expect(out).toContain('def f(): pass');
  });
});


describe('OptionsBlock — edge cases', () => {
  it('handles an empty body without crashing or breaking the border', () => {
    const out = strip(
      render(
        <OptionsBlock
          options={[
            { title: 'Skip', body: '' },
            { title: 'Apply', body: 'do it' },
          ]}
        />,
      ).lastFrame(),
    );
    expect(out).toContain(TOP_LEFT);
    expect(out).toContain(BOTTOM_LEFT);
    expect(out).toContain('A.  Skip');
    expect(out).toContain('do it');
  });

  it('handles a no-break long word (wraps mid-word at column boundary)', () => {
    // Should not crash; should render some prefix of the word in the box.
    const word = 'supercalifragilisticexpialidocious_with_a_lot_more_unbreakable_chars';
    const out = strip(
      render(
        <OptionsBlock
          options={[
            { title: 'A', body: word },
            { title: 'B', body: 'normal' },
          ]}
        />,
      ).lastFrame(),
    );
    // Some part of the word should appear.
    expect(out).toContain(word.slice(0, 20));
  });

  it('renders a body that is only a diff', () => {
    const out = strip(
      render(
        <OptionsBlock
          options={[
            { title: 'A', body: '```diff\n+++ a.py\n@@ -0,0 +1,1 @@\n+x = 1\n```' },
            { title: 'B', body: '```diff\n+++ a.py\n@@ -0,0 +1,1 @@\n+x = 2\n```' },
          ]}
        />,
      ).lastFrame(),
    );
    expect(out).toContain('x = 1');
    expect(out).toContain('x = 2');
  });
});
