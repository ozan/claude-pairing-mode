// Custom input field built on Ink's `useInput`. We manage our own buffer +
// cursor + history so we get readline-ish behaviour (ctrl-a/e/b/f/k/u/w,
// arrow-key cursor + history) without depending on @inkjs/ui TextInput.
//
// History is owned by the parent (App) so it survives this component's
// remount on each submit; we receive it as a prop and only navigate locally.

import React, { useState } from 'react';
import { Box, Text, useInput } from 'ink';

const SOFT_WHITE = '#c0c5cc';

// Find the start index of the previous word from `cursor`, skipping any
// trailing whitespace at `cursor` first. Used for ctrl-w / ctrl-leftarrow.
function prevWordStart(value: string, cursor: number): number {
  let i = cursor;
  while (i > 0 && /\s/.test(value[i - 1]!)) i--;
  while (i > 0 && !/\s/.test(value[i - 1]!)) i--;
  return i;
}

export function ChatInput({
  isDisabled,
  onSubmit,
  history = [],
}: {
  isDisabled: boolean;
  onSubmit: (text: string) => void;
  /** Submitted lines, oldest first. Up/ctrl-p walks backward through this. */
  history?: string[];
}) {
  const [value, setValue] = useState('');
  const [cursor, setCursor] = useState(0);
  // -1 means "editing current draft"; 0..history.length-1 indexes from the
  // newest end of history (0 = most recent submitted entry).
  const [historyIdx, setHistoryIdx] = useState(-1);
  // Saved draft when the user stepped from -1 into history. Restored on the
  // way back out so an in-progress line isn't lost by browsing.
  const [savedDraft, setSavedDraft] = useState('');

  const setBuffer = (next: string, nextCursor?: number) => {
    setValue(next);
    setCursor(nextCursor ?? next.length);
    setHistoryIdx(-1);
  };

  const navigateHistory = (direction: 1 | -1) => {
    // direction: 1 = older (toward index 0), -1 = newer (toward draft).
    if (history.length === 0) return;
    let nextIdx: number;
    if (direction === 1) {
      if (historyIdx >= history.length - 1) return; // already at oldest
      nextIdx = historyIdx + 1;
      if (historyIdx === -1) setSavedDraft(value);
    } else {
      if (historyIdx === -1) return; // already at draft
      nextIdx = historyIdx - 1;
    }
    const nextValue =
      nextIdx === -1 ? savedDraft : history[history.length - 1 - nextIdx]!;
    setValue(nextValue);
    setCursor(nextValue.length);
    setHistoryIdx(nextIdx);
  };

  useInput(
    (input, key) => {
      if (isDisabled) return;

      // Pasted/batched input may include the Enter byte (\r or \n) inline,
      // even though Ink's `key.return` flag is false. Split and treat the
      // newline as a submit boundary.
      if (input && (input.includes('\r') || input.includes('\n')) && !key.ctrl && !key.meta) {
        const cutIdx = (() => {
          const cr = input.indexOf('\r');
          const lf = input.indexOf('\n');
          if (cr === -1) return lf;
          if (lf === -1) return cr;
          return Math.min(cr, lf);
        })();
        const before = input.slice(0, cutIdx);
        const after = input.slice(cutIdx + 1);
        const submission = (value + before).trim();
        if (submission) {
          onSubmit(submission);
          setBuffer(after);
        } else {
          setBuffer(after);
        }
        return;
      }

      if (key.return) {
        if (value.trim()) {
          onSubmit(value);
          setBuffer('');
        }
        return;
      }

      // Readline-style ctrl bindings. Handle BEFORE the generic key.ctrl
      // bail-out, since input here is the bare letter (e.g. 'a' for ctrl-a).
      if (key.ctrl) {
        if (input === 'a') { setCursor(0); return; }
        if (input === 'e') { setCursor(value.length); return; }
        if (input === 'b') { setCursor(Math.max(0, cursor - 1)); return; }
        if (input === 'f') { setCursor(Math.min(value.length, cursor + 1)); return; }
        if (input === 'k') {
          setBuffer(value.slice(0, cursor), cursor);
          return;
        }
        if (input === 'u') {
          setBuffer(value.slice(cursor), 0);
          return;
        }
        if (input === 'w') {
          const start = prevWordStart(value, cursor);
          setBuffer(value.slice(0, start) + value.slice(cursor), start);
          return;
        }
        if (input === 'p') { navigateHistory(1); return; }
        if (input === 'n') { navigateHistory(-1); return; }
        // Other ctrl combos (incl. ctrl-c, ctrl-d) — let Ink handle.
        return;
      }
      if (key.meta) return;

      if (key.backspace || key.delete) {
        if (cursor === 0) return;
        setBuffer(value.slice(0, cursor - 1) + value.slice(cursor), cursor - 1);
        return;
      }
      if (key.leftArrow) { setCursor(Math.max(0, cursor - 1)); return; }
      if (key.rightArrow) { setCursor(Math.min(value.length, cursor + 1)); return; }
      if (key.upArrow) { navigateHistory(1); return; }
      if (key.downArrow) { navigateHistory(-1); return; }
      if (key.escape || key.tab || key.pageDown || key.pageUp) return;

      if (input) {
        const next = value.slice(0, cursor) + input + value.slice(cursor);
        setBuffer(next, cursor + input.length);
      }
    },
    { isActive: !isDisabled },
  );

  // Render with the cursor block sitting on the character at `cursor` (or a
  // trailing space if cursor is at end-of-line).
  const before = value.slice(0, cursor);
  const atCursor = value[cursor] ?? ' ';
  const after = value.slice(cursor + 1);

  return (
    <Box>
      <Text color={SOFT_WHITE}>❯ </Text>
      <Text>{before}</Text>
      {!isDisabled ? <Text inverse>{atCursor}</Text> : <Text>{atCursor === ' ' ? '' : atCursor}</Text>}
      <Text>{after}</Text>
    </Box>
  );
}
