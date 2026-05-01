// Custom input field built on Ink's `useInput`. We manage our own buffer +
// cursor, so we know Enter is captured exactly the way we expect (no
// dependency on @inkjs/ui TextInput's behavior, which doesn't seem to dispatch
// onSubmit reliably under our setup).

import React, { useState } from 'react';
import { Box, Text, useInput } from 'ink';

const SOFT_WHITE = '#c0c5cc';

export function ChatInput({
  isDisabled,
  onSubmit,
}: {
  isDisabled: boolean;
  onSubmit: (text: string) => void;
}) {
  const [value, setValue] = useState('');

  useInput(
    (input, key) => {
      if (isDisabled) return;
      // Pasted/batched input may include the Enter byte (\r or \n) inline,
      // even though Ink's `key.return` flag is false. Split and treat the
      // newline as a submit boundary.
      if (input && (input.includes('\r') || input.includes('\n'))) {
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
          setValue(after);
        } else {
          setValue(after);
        }
        return;
      }

      if (key.return) {
        if (value.trim()) {
          onSubmit(value);
          setValue('');
        }
        return;
      }
      if (key.backspace || key.delete) {
        setValue((v) => v.slice(0, -1));
        return;
      }
      if (key.ctrl || key.meta) return;
      // Ignore arrow keys and similar.
      if (
        key.upArrow ||
        key.downArrow ||
        key.leftArrow ||
        key.rightArrow ||
        key.escape ||
        key.tab ||
        key.pageDown ||
        key.pageUp
      ) {
        return;
      }
      if (input) {
        setValue((v) => v + input);
      }
    },
    { isActive: !isDisabled },
  );

  return (
    <Box>
      <Text color={SOFT_WHITE}>❯ </Text>
      <Text>{value}</Text>
      {!isDisabled ? <Text inverse> </Text> : null}
    </Box>
  );
}
