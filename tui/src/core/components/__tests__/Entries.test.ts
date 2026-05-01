import { describe, expect, it } from 'bun:test';
import { shortToolName, summarizeInput } from '../Entries';

describe('shortToolName', () => {
  it('returns "tool" for empty/missing name', () => {
    expect(shortToolName('')).toBe('tool');
  });

  it('strips the mcp__server__ prefix', () => {
    expect(shortToolName('mcp__proto_pair__propose_options')).toBe('propose_options');
  });

  it('renames Edit to Update (CC convention)', () => {
    expect(shortToolName('Edit')).toBe('Update');
  });

  it('passes through other tool names unchanged', () => {
    expect(shortToolName('Bash')).toBe('Bash');
    expect(shortToolName('Read')).toBe('Read');
    expect(shortToolName('Glob')).toBe('Glob');
  });
});

describe('summarizeInput', () => {
  it('returns empty for null/undefined/non-object', () => {
    expect(summarizeInput(null)).toBe('');
    expect(summarizeInput(undefined)).toBe('');
    expect(summarizeInput('foo')).toBe('');
    expect(summarizeInput(42)).toBe('');
  });

  it('returns empty for empty object (avoids `({})` flicker mid-stream)', () => {
    expect(summarizeInput({})).toBe('');
  });

  it('prefers `command` field for Bash', () => {
    expect(summarizeInput({ command: 'ls' })).toBe('ls');
    expect(summarizeInput({ command: 'ls', timeout: 5 })).toBe('ls');
  });

  it('prefers `file_path` field for Read/Edit/Write', () => {
    expect(summarizeInput({ file_path: 'foo.py' })).toBe('foo.py');
    expect(summarizeInput({ file_path: 'a.py', old_string: 'x', new_string: 'y' })).toBe('a.py');
  });

  it('truncates long values with an ellipsis', () => {
    const long = 'x'.repeat(150);
    const out = summarizeInput({ command: long });
    expect(out.length).toBeLessThanOrEqual(81);
    expect(out.endsWith('…')).toBe(true);
  });

  it('returns empty for objects with only unrecognized keys (no JSON dump)', () => {
    // Don't render `({"some_obscure_param":42})` — empty parens are nicer.
    expect(summarizeInput({ obscure: 42 })).toBe('');
  });
});
