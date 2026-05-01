import React from 'react';
import { describe, expect, it } from 'bun:test';
import { render } from 'ink-testing-library';
import { OptionsBlock } from '../OptionsBlock';

function stripAnsi(s: string | undefined): string {
  if (!s) return '';
  return s.replace(/\x1B\[[0-9;]*[A-Za-z]/g, '');
}

describe('OptionsBlock', () => {
  it('renders both option titles in two columns', () => {
    const { lastFrame } = render(
      <OptionsBlock
        options={[
          { title: 'Recursive', body: 'first body' },
          { title: 'Iterative', body: 'second body' },
        ]}
      />,
    );
    const out = stripAnsi(lastFrame());
    expect(out).toContain('A.');
    expect(out).toContain('Recursive');
    expect(out).toContain('B.');
    expect(out).toContain('Iterative');
  });

  it('renders option bodies', () => {
    const { lastFrame } = render(
      <OptionsBlock
        options={[
          { title: 'A', body: 'alpha body' },
          { title: 'B', body: 'beta body' },
        ]}
      />,
    );
    const out = stripAnsi(lastFrame());
    expect(out).toContain('alpha body');
    expect(out).toContain('beta body');
  });
});
