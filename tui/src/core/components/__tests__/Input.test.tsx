// Render-level tests for ChatInput's readline-style bindings. We drive
// keystrokes via ink-testing-library's stdin.write — Ink's useInput maps the
// raw bytes to (input, key) just like a real terminal would.

import React from 'react';
import { describe, expect, it } from 'bun:test';
import { render } from 'ink-testing-library';
import { ChatInput } from '../Input';

const ANSI = /\x1B\[[0-9;]*[A-Za-z]/g;

/**
 * Pull the literal value out of the rendered prompt line. The cursor is
 * rendered as an inverse-video block (`\x1B[7m X \x1B[27m`); when the cursor
 * is at end-of-buffer, X is a phantom space that we drop. Otherwise we
 * splice it back in at its position.
 */
function visibleBuffer(frame: string | undefined): string {
  if (!frame) return '';
  const promptIdx = frame.indexOf('❯ ');
  if (promptIdx === -1) return '';
  const tail = frame.slice(promptIdx + 2);
  const eol = tail.indexOf('\n');
  const line = eol === -1 ? tail : tail.slice(0, eol);

  const m = line.match(/^([\s\S]*?)\x1B\[7m([\s\S]*?)\x1B\[27m([\s\S]*?)$/);
  if (!m) return line.replace(ANSI, '');

  const before = m[1]!.replace(ANSI, '');
  const at = m[2]!.replace(ANSI, '');
  const after = m[3]!.replace(ANSI, '');
  if (after === '' && at === ' ') return before; // cursor at end-of-buffer
  return before + at + after;
}

// Tiny sleep so React state updates flush between input writes. Without it
// rapid sequential writes can race.
const tick = () => new Promise((r) => setTimeout(r, 10));

// Send keys one at a time with a tick between them — Ink batches simultaneous
// stdin bytes into a single useInput event, so e.g. \x06\x06 arrives as
// input='\x06\x06' rather than two ctrl-f presses. Real terminal use sends
// one byte per keypress, so this is the realistic mode to test.
async function press(stdin: { write: (s: string) => unknown }, ...keys: string[]) {
  for (const k of keys) {
    stdin.write(k);
    await tick();
  }
}


describe('ChatInput — basic typing', () => {
  it('inserts characters at the cursor', async () => {
    const { stdin, lastFrame } = render(
      <ChatInput isDisabled={false} onSubmit={() => {}} />,
    );
    await press(stdin, 'hello');
    expect(visibleBuffer(lastFrame())).toBe('hello');
  });

  it('backspace deletes the char before the cursor', async () => {
    const { stdin, lastFrame } = render(
      <ChatInput isDisabled={false} onSubmit={() => {}} />,
    );
    await press(stdin, 'hello', '\x7f');
    expect(visibleBuffer(lastFrame())).toBe('hell');
  });
});


describe('ChatInput — readline cursor bindings', () => {
  it('ctrl-a moves cursor to the start; subsequent typing inserts there', async () => {
    const { stdin, lastFrame } = render(
      <ChatInput isDisabled={false} onSubmit={() => {}} />,
    );
    await press(stdin, 'world', '\x01', 'h', 'i', ' ');
    expect(visibleBuffer(lastFrame())).toBe('hi world');
  });

  it('ctrl-e moves cursor to the end', async () => {
    const { stdin, lastFrame } = render(
      <ChatInput isDisabled={false} onSubmit={() => {}} />,
    );
    await press(stdin, 'world', '\x01', '\x05', '!');
    expect(visibleBuffer(lastFrame())).toBe('world!');
  });

  it('ctrl-k kills from cursor to end of line', async () => {
    const { stdin, lastFrame } = render(
      <ChatInput isDisabled={false} onSubmit={() => {}} />,
    );
    await press(stdin, 'hello world', '\x01');
    // ctrl-f five times → cursor at index 5 (just after "hello").
    await press(stdin, '\x06', '\x06', '\x06', '\x06', '\x06');
    await press(stdin, '\x0b'); // ctrl-k
    expect(visibleBuffer(lastFrame())).toBe('hello');
  });

  it('ctrl-u kills from start to cursor', async () => {
    const { stdin, lastFrame } = render(
      <ChatInput isDisabled={false} onSubmit={() => {}} />,
    );
    await press(stdin, 'hello world', '\x01');
    // ctrl-f six times → cursor at index 6 (just after "hello ").
    await press(stdin, '\x06', '\x06', '\x06', '\x06', '\x06', '\x06');
    await press(stdin, '\x15'); // ctrl-u
    expect(visibleBuffer(lastFrame())).toBe('world');
  });

  it('ctrl-w deletes the previous word (cursor lands after the trailing space)', async () => {
    // Ink trims trailing whitespace from rendered text, so we can't observe
    // the trailing space directly. Type a char after ctrl-w — its position
    // proves the cursor was placed after the kept space.
    const { stdin, lastFrame } = render(
      <ChatInput isDisabled={false} onSubmit={() => {}} />,
    );
    await press(stdin, 'foo bar baz', '\x17', 'X');
    expect(visibleBuffer(lastFrame())).toBe('foo bar X');
  });
});


describe('ChatInput — history', () => {
  it('ctrl-p / ctrl-n walks through prior submissions', async () => {
    const { stdin, lastFrame } = render(
      <ChatInput isDisabled={false} onSubmit={() => {}} history={['first', 'second']} />,
    );
    await press(stdin, '\x10'); // ctrl-p
    expect(visibleBuffer(lastFrame())).toBe('second');
    await press(stdin, '\x10'); // ctrl-p
    expect(visibleBuffer(lastFrame())).toBe('first');
    await press(stdin, '\x0e'); // ctrl-n
    expect(visibleBuffer(lastFrame())).toBe('second');
    await press(stdin, '\x0e'); // ctrl-n → back to draft (empty)
    expect(visibleBuffer(lastFrame())).toBe('');
  });

  it('preserves an in-progress draft when stepping into history and back', async () => {
    const { stdin, lastFrame } = render(
      <ChatInput isDisabled={false} onSubmit={() => {}} history={['old']} />,
    );
    await press(stdin, 'drafting', '\x10'); // type, then ctrl-p
    expect(visibleBuffer(lastFrame())).toBe('old');
    await press(stdin, '\x0e'); // ctrl-n → restore draft
    expect(visibleBuffer(lastFrame())).toBe('drafting');
  });
});
