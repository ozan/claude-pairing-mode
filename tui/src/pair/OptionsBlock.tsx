// Two-column option panel — the choice-based pair-programmer experiment's
// only piece of UI. Each option lives in a rounded-border box, padding 1,
// with the title bold inside and the body markdown below it.
//
// Layout:
//   - Outer Box flexDirection="row" with no flex-basis percentages — Ink's
//     percentage flex-basis interacts badly with column gaps and borders
//     and overflows by 1-2 cols. Instead we read the terminal width via
//     useStdout and split it explicitly.
//   - alignItems="stretch" so both panels are equal height regardless of
//     content (shorter side has trailing empty rows inside its border).
//   - padding={1} + borderStyle="round" gives 1 char of border + 1 char of
//     padding on each side → content area is panelWidth - 4.

import React, { memo, useEffect, useMemo, useState } from 'react';
import { Box, Text, useStdout } from 'ink';
import wrapAnsi from 'wrap-ansi';
import { Markdown, splitBlocks } from '../core/components/Markdown.js';

const BORDER_COLOR = '#5c6370';
const GAP = 2; // columns of space between the two panels


// Pre-wrap prose paragraphs in the body using wrap-ansi with `trim: true` so
// continuation lines don't keep a leading space (Ink's own wrap uses
// `trim: false`, which is why we see ` the op...` after `Recursi...`). Fenced
// blocks are left intact — the diff renderer handles its own layout.
function prewrapBody(body: string, width: number): string {
  if (width < 4) return body;
  return splitBlocks(body)
    .map((b) => {
      if (b.kind === 'fence') return '```' + b.lang + '\n' + b.body + '\n```';
      return wrapAnsi(b.text, width, { trim: true, hard: true });
    })
    .join('\n');
}

/** Re-renders when the terminal width changes. Ink's useStdout doesn't
 * subscribe to resize events on its own, so we hook the underlying
 * stdout's `resize` event ourselves and trigger a re-render. */
function useTerminalCols(): number {
  const { stdout } = useStdout();
  const [cols, setCols] = useState<number>(stdout?.columns ?? 80);
  useEffect(() => {
    if (!stdout) return;
    const onResize = () => setCols(stdout.columns ?? 80);
    stdout.on('resize', onResize);
    return () => {
      stdout.off('resize', onResize);
    };
  }, [stdout]);
  return cols;
}

export const OptionsBlock = memo(function OptionsBlock({
  options,
}: {
  options: { title: string; body: string }[];
}) {
  const cols = useTerminalCols();
  // Total available cols. Subtract the gap (one fewer than panel count),
  // then floor-divide. Floor leaves a few cols unused on odd-width
  // terminals — that's fine; preferable to overflow.
  const panelWidth = Math.floor((cols - GAP * (options.length - 1)) / options.length);
  // Inner content width: minus 2 for the rounded border, 2 for paddingX={1}.
  const contentWidth = Math.max(0, panelWidth - 4);

  const wrappedBodies = useMemo(
    () => options.map((opt) => prewrapBody(opt.body, contentWidth)),
    [options, contentWidth],
  );

  return (
    <Box flexDirection="row" marginTop={1} alignItems="stretch">
      {options.map((opt, i) => {
        const letter = String.fromCharCode(65 + i);
        const isLast = i === options.length - 1;
        return (
          <Box
            key={i}
            flexDirection="column"
            width={panelWidth}
            marginRight={isLast ? 0 : GAP}
            borderStyle="round"
            borderColor={BORDER_COLOR}
            paddingX={1}
            paddingY={0}
          >
            <Text bold>
              {letter}.  {opt.title}
            </Text>
            <Box height={1} />
            <Markdown src={wrappedBodies[i]!} />
          </Box>
        );
      })}
    </Box>
  );
});
